# WmData.py

import sys
import Xlib.X as X
import Xlib.XK as XK

################################################################################

class WmDataStack(object):

    def __init__(self, config):

        self.border_width = config.stack.border_width

################################################################################

class WmDataTab(object):

    def __init__(self, display, screen, config):

        self.border_width = config.tab.border_width

        font = display.open_font(config.tab.font)
        query = font.query()
        font_height = query.font_ascent + query.font_descent

        self.height = font_height + config.tab.border_width * 2 + config.tab.padding * 2
        self.font_y_offset = font_height + config.tab.padding

        colormap = screen.default_colormap

        fg = colormap.alloc_named_color(config.tab.ff_fg).pixel
        bg = colormap.alloc_named_color(config.tab.ff_bg).pixel
        self.ff_gc = screen.root.create_gc(font=font, foreground=fg, background=bg)
        self.ff_border = colormap.alloc_named_color(self.ff_bo).pixel

        fg = colormap.alloc_named_color(config.tab.fu_fg).pixel
        bg = colormap.alloc_named_color(config.tab.fu_bg).pixel
        self.fu_gc = screen.root.create_gc(font=font, foreground=fg, background=bg)
        self.fu_border = colormap.alloc_named_color(self.fu_bo).pixel

        fg = colormap.alloc_named_color(config.tab.uf_fg).pixel
        bg = colormap.alloc_named_color(config.tab.uf_bg).pixel
        self.uf_gc = screen.root.create_gc(font=font, foreground=fg, background=bg)
        self.uf_border = colormap.alloc_named_color(self.uf_bo).pixel

        fg = colormap.alloc_named_color(config.tab.uu_fg).pixel
        bg = colormap.alloc_named_color(config.tab.uu_bg).pixel
        self.uu_gc = screen.root.create_gc(font=font, foreground=fg, background=bg)
        self.uu_border = colormap.alloc_named_color(self.uu_bo).pixel

################################################################################

class WmDataStatusBar(object):

    def __init__(self, display, screen, config):

        self.border_width = config.status_bar.border_width

        colormap = screen.default_colormap

        bg = colormap.alloc_named_color(config.status_bar.ff_bg).pixel
        self.gc = screen.root.create_gc(background=bg)
        self.border = colormap.alloc_named_color(self.ff_bo).pixel

################################################################################

class WmDataGroup(object):

    def __init__(self, display, screen, config):

        self.border_width = config.group.border_width

        font = display.open_font(config.group.font)
        query = font.query()
        font_height = query.font_ascent + query.font_descent

        self.height = font_height + config.group.border_width * 2 + config.group.padding * 2
        self.font_y_offset = font_height + config.group.padding

        colormap = screen.default_colormap

        fg = colormap.alloc_named_color(config.group.active_fg).pixel
        bg = colormap.alloc_named_color(config.group.active_bg).pixel
        self.active_gc = screen.root.create_gc(font=font, foreground=fg, background=bg)
        self.active_border = colormap.alloc_named_color(self.active_bo).pixel

        fg = colormap.alloc_named_color(config.group.inactive_fg).pixel
        bg = colormap.alloc_named_color(config.group.inactive_bg).pixel
        self.inactive_gc = screen.root.create_gc(font=font, foreground=fg, background=bg)
        self.inactive_border = colormap.alloc_named_color(self.inactive_bo).pixel

################################################################################

class WmDataMeter(object):

    def __init__(self, display, screen, config):

        self.border_width = config.meter.border_width

        font = display.open_font(config.meter.font)
        query = font.query()
        font_height = query.font_ascent + query.font_descent

        self.height = font_height + config.meter.border_width * 2 + config.meter.padding * 2
        self.font_y_offset = font_height + config.meter.padding

        colormap = screen.default_colormap

        fg = colormap.alloc_named_color(config.meter.fg).pixel
        bg = colormap.alloc_named_color(config.meter.bg).pixel
        self.gc = screen.root.create_gc(font=font, foreground=fg, background=bg)
        self.border = colormap.alloc_named_color(self.bo).pixel

################################################################################

class WmDataAtoms(object):
    pass

################################################################################

class WmData(object):

    def __init__(self, display, screen, config):

        self.display = display
        self.screen = screen
        self.root = screen.root
        self.config = config

        self.stack = WmDataStack(display, screen, config)
        self.tab = WmDataTab(display, screen, config)
        self.status_bar = WmDataStatusBar(display, screen, config)
        self.group = WmDataGroup(display, screen, config)
        self.meter = WmDataMeter(display, screen, config)

        self.keymap = {}
        self.parse_keys(display, config.keys)

        self.setup_atoms()

    ############################################################################

    def parse_keys(self, display, config):

        commands = ['next_window',
                    'prev_window',
                    'kill_window']

        for command in commands:

            key_def = getattr(config.keys, command)
            (modifier, key) = key_def.split('+')  # TODO Handle multiple modifiers

            if modifier == 'mod4':
                mod_mask = X.Mod4Mask
            elif modifier == 'mod3':
                mod_mask = X.Mod3Mask
            elif modifier == 'mod2':
                mod_mask = X.Mod2Mask
            elif modifier == 'mod1':
                mod_mask = X.Mod1Mask
            else:
                print "Command '%s' uses unknown modifier '%s'" % (command, modifier)
                sys.exit(1)

            keycode = display.keysym_to_keycode(XK.string_to_keysym(key))
            self.keymap[(mod_mask, keycode)] = command

    ############################################################################

    def setup_atoms(self):

        self.atoms = WmDataAtoms()
        self.atoms.WM_PROTOCOLS = self.display.intern_atom('WM_PROTOCOLS')
        self.atoms.WM_DELETE_WINDOW = self.display.intern_atom('WM_DELETE_WINDOW')
