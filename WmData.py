# WmData.py

import sys
import Xlib.X as X
import Xlib.XK as XK

################################################################################

class WmDataStack(object):

    def __init__(self, dispaly, screen, config):

        self.border_width = config.stack.border_width

################################################################################

class WmDataTab(object):

    def __init__(self, display, screen, config):

        self.border_width = config.tab.border_width

        font = display.open_font(config.tab.font)
        query = font.query()
        font_height = query.font_ascent + query.font_descent

        self.height = font_height + config.tab.border_width * 2 + config.tab.padding * 2
        self.font_y_offset = font_height - 2 * config.tab.padding

        colormap = screen.default_colormap

        fg = colormap.alloc_named_color(config.tab.ff_fg).pixel
        self.ff_bg = colormap.alloc_named_color(config.tab.ff_bg).pixel
        self.ff_gc = screen.root.create_gc(font=font, foreground=fg, background=self.ff_bg)
        self.ff_bo = colormap.alloc_named_color(config.tab.ff_bo).pixel

        fg = colormap.alloc_named_color(config.tab.fu_fg).pixel
        self.fu_bg = colormap.alloc_named_color(config.tab.fu_bg).pixel
        self.fu_gc = screen.root.create_gc(font=font, foreground=fg, background=self.fu_bg)
        self.fu_bo = colormap.alloc_named_color(config.tab.fu_bo).pixel

        fg = colormap.alloc_named_color(config.tab.uf_fg).pixel
        self.uf_bg = colormap.alloc_named_color(config.tab.uf_bg).pixel
        self.uf_gc = screen.root.create_gc(font=font, foreground=fg, background=self.uf_bg)
        self.uf_bo = colormap.alloc_named_color(config.tab.uf_bo).pixel

        fg = colormap.alloc_named_color(config.tab.uu_fg).pixel
        self.uu_bg = colormap.alloc_named_color(config.tab.uu_bg).pixel
        self.uu_gc = screen.root.create_gc(font=font, foreground=fg, background=self.uu_bg)
        self.uu_bo = colormap.alloc_named_color(config.tab.uu_bo).pixel

################################################################################

class WmDataStatusBar(object):

    def __init__(self, display, screen, config):

        self.border_width = config.status_bar.border_width

        colormap = screen.default_colormap

        self.bg = colormap.alloc_named_color(config.status_bar.bg).pixel
        self.gc = screen.root.create_gc(background=self.bg)
        self.bo = colormap.alloc_named_color(config.status_bar.bo).pixel

################################################################################

class WmDataGroup(object):

    def __init__(self, display, screen, config):

        self.border_width = config.group.border_width
        self.padding = config.group.padding

        font = display.open_font(config.group.font)
        query = font.query()
        font_height = query.font_ascent + query.font_descent

        self.height = font_height + config.group.border_width * 2 + config.group.padding * 2
        self.font_y_offset = font_height - 2 * config.group.padding

        colormap = screen.default_colormap

        fg = colormap.alloc_named_color(config.group.f_fg).pixel
        self.f_bg = colormap.alloc_named_color(config.group.f_bg).pixel
        self.f_gc = screen.root.create_gc(font=font, foreground=fg, background=self.f_bg)
        self.f_bo = colormap.alloc_named_color(config.group.f_bo).pixel

        fg = colormap.alloc_named_color(config.group.u_fg).pixel
        self.u_bg = colormap.alloc_named_color(config.group.u_bg).pixel
        self.u_gc = screen.root.create_gc(font=font, foreground=fg, background=self.u_bg)
        self.u_bo = colormap.alloc_named_color(config.group.u_bo).pixel

################################################################################

class WmDataMeter(object):

    def __init__(self, display, screen, config):

        self.border_width = config.meter.border_width
        self.padding = config.meter.padding

        font = display.open_font(config.meter.font)
        query = font.query()
        font_height = query.font_ascent + query.font_descent

        self.height = font_height + config.meter.border_width * 2 + config.meter.padding * 2
        self.font_y_offset = font_height - 2 * config.meter.padding

        colormap = screen.default_colormap

        fg = colormap.alloc_named_color(config.meter.fg).pixel
        self.bg = colormap.alloc_named_color(config.meter.bg).pixel
        self.gc = screen.root.create_gc(font=font, foreground=fg, background=self.bg)
        self.bo = colormap.alloc_named_color(config.meter.bo).pixel

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

        self.status_bar.height = max(self.group.height, self.meter.height)

        self.keymap = {}
        self.parse_keys(display, config)

        self.setup_atoms()

    ############################################################################

    def parse_keys(self, display, config):

        commands = ['next_window',
                    'prev_window',
                    'kill_window',
                    'split_horizontal',
                    'split_vertical',
                    'next_stack',
                    'prev_stack',
                    'kill_stack']

        for command in commands:

            key_def = getattr(config.keys, command)
            (modifier, key) = key_def.split('+')  # TODO Handle multiple modifiers

            if modifier == 'Mod4':
                mod_mask = X.Mod4Mask
            elif modifier == 'Mod3':
                mod_mask = X.Mod3Mask
            elif modifier == 'Mod2':
                mod_mask = X.Mod2Mask
            elif modifier == 'Mod1':
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
