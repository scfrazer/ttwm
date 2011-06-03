# WmScreen.py

import Xlib.X as X
import Xlib.error as Xerror
import sys
from WmGroup import WmGroup

class WmScreen(object):

    def __init__(self, display, screen, config):

        self.display = display
        self.root = screen.root
        self.config = config

        self.get_root()
        self.setup_colors(screen)
        self.setup_gcs()
        self.grab_keys()

        self.groups = {'Default': WmGroup(self.display, self.root, self.config,
                                          self.pixel_colors, self.gcs,
                                          claim_all_windows=True)}

    ############################################################################

    def get_root(self):

        catch = Xerror.CatchError(Xerror.BadAccess)
        self.root.change_attributes(event_mask=(X.PropertyChangeMask
                                                | X.FocusChangeMask
                                                | X.SubstructureRedirectMask
                                                | X.SubstructureNotifyMask),
                                    onerror=catch)
        self.display.sync()
        if catch.get_error():
            print "Another window manager is already runing"
            sys.exit(1)

    ############################################################################

    def setup_colors(self, screen):

        self.pixel_colors = {}

        colormap = screen.default_colormap

        for (color_name, color_value) in self.config.colors.iteritems():
            color = colormap.alloc_named_color(color_value)
            self.pixel_colors[color_name] = color.pixel

    ############################################################################

    def setup_gcs(self):

        self.gcs = {}

        font = self.display.open_font(self.config.fonts['title'])

        query = font.query()
        # TODO 6 = 2 pad + 1 border on top/bottom ... should be configurable
        self.config.display['tab_height'] = query.font_ascent + query.font_descent + 6

        for name in ['active_selected', 'active_unselected',
                     'inactive_selected', 'inactive_unselected']:

            self.gcs[name] = self.root.create_gc(font=font,
                                                 foreground=self.pixel_colors[name + '_fg'],
                                                 background=self.pixel_colors[name + '_bg'])

    ############################################################################

    def grab_keys(self):

        release_mod = X.AnyModifier << 1
        for item in self.config.keys:
            (mod_mask, keycode) = item
            self.root.grab_key(keycode, mod_mask & ~release_mod,
                               1, X.GrabModeAsync, X.GrabModeAsync)

    ############################################################################

    def handle_key_press(self, event):
        lookup = (event.state, event.detail)
        # TODO
        if lookup in self.config.keys:
            print self.config.keys[lookup]
