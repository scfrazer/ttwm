# WmScreen.py

import Xlib.X
import Xlib.error
import Xlib.XK
import sys
from WmGroup import WmGroup

class WmScreen(object):

    def __init__(self, display, screen, config):

        self.display = display
        self.root = screen.root
        self.config = config

        self.get_root()
        self.grab_keys()

        self.groups = {
            'Default': WmGroup(self.display, self.root, self.config, claim_all_windows=True)
            }

    ############################################################################

    def get_root(self):

        catch = Xlib.error.CatchError(Xlib.error.BadAccess)
        self.root.change_attributes(event_mask=(Xlib.X.EnterWindowMask
                                                | Xlib.X.LeaveWindowMask
                                                | Xlib.X.PropertyChangeMask
                                                | Xlib.X.FocusChangeMask
                                                | Xlib.X.SubstructureRedirectMask
                                                | Xlib.X.SubstructureNotifyMask),
                                    onerror=catch)
        self.display.sync()
        if catch.get_error():
            print "Another window manager is already runing"
            sys.exit(1)

    ############################################################################

    def grab_keys(self):

        release_mod = Xlib.X.AnyModifier << 1
        for item in self.config.keymap:
            (mod_mask, keycode) = item
            self.root.grab_key(keycode, mod_mask & ~release_mod,
                               1, Xlib.X.GrabModeAsync, Xlib.X.GrabModeAsync)

    ############################################################################

    def handle_key_press(self, event):
        lookup = (event.state, event.detail)
        if lookup in self.config.keymap:
            print self.config.keymap[lookup]
