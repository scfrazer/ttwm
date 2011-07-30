# WmConfig.py

import sys
import logging
import ConfigParser
import Xlib.X as X
import Xlib.XK as XK

################################################################################

class WmConfigDisplay(object):

    def __init__(self):

        self.border_width = 1

################################################################################

class WmConfigColors(object):

    def __init__(self):

        self.tab_ff_fg = '#ffffff'
        self.tab_ff_bg = '#607080'
        self.tab_ff_bo = '#708090'

        self.tab_fu_fg = '#a0a0a0'
        self.tab_fu_bg = '#405060'
        self.tab_fu_bo = '#607080'

        self.tab_uf_fg = '#c0c0c0'
        self.tab_uf_bg = '#405060'
        self.tab_uf_bo = '#607080'

        self.tab_uu_fg = '#a0a0a0'
        self.tab_uu_bg = '#304050'
        self.tab_uu_bo = '#506070'

    def pixelize_colors(self, screen):

        colormap = screen.default_colormap

        self.tab_ff_fg = colormap.alloc_named_color(self.tab_ff_fg).pixel
        self.tab_ff_bg = colormap.alloc_named_color(self.tab_ff_bg).pixel
        self.tab_ff_bo = colormap.alloc_named_color(self.tab_ff_bo).pixel

        self.tab_fu_fg = colormap.alloc_named_color(self.tab_fu_fg).pixel
        self.tab_fu_bg = colormap.alloc_named_color(self.tab_fu_bg).pixel
        self.tab_fu_bo = colormap.alloc_named_color(self.tab_fu_bo).pixel

        self.tab_uf_fg = colormap.alloc_named_color(self.tab_uf_fg).pixel
        self.tab_uf_bg = colormap.alloc_named_color(self.tab_uf_bg).pixel
        self.tab_uf_bo = colormap.alloc_named_color(self.tab_uf_bo).pixel

        self.tab_uu_fg = colormap.alloc_named_color(self.tab_uu_fg).pixel
        self.tab_uu_bg = colormap.alloc_named_color(self.tab_uu_bg).pixel
        self.tab_uu_bo = colormap.alloc_named_color(self.tab_uu_bo).pixel

################################################################################

class WmConfigFonts(object):

    def __init__(self):

        self.title = '-*-helvetica-medium-r-*-*-12-*'
        self.group = '-*-helvetica-medium-r-*-*-14-*'

################################################################################

class WmConfig(object):

    def __init__(self, display):

        config = self.read_config_file()

        self.parse_display(config)
        self.parse_colors(config)
        self.parse_fonts(config)

        self.keys = {}
        self.parse_keys(display, config)

    ############################################################################

    def read_config_file(self):

        filename = '.ttwmrc'  # TODO Find this in various places

        try:
            config_file = open(filename)
        except IOError:
            print "\nError: Couldn't read '%s'\n" % (filename)
            return

        logging.debug("Reading config file '%s'", config_file.name)
        config = ConfigParser.RawConfigParser()
        config.readfp(config_file)
        config_file.close()

        return config

    ############################################################################

    def parse_display(self, config):

        self.display = WmConfigDisplay()

        section = 'Display'

        if section not in config.sections():
            return

        for option in config.options(section):
            if not hasattr(self.display, option):
                print "Unknown option '%s' in '%s' section" % (option, section)
                sys.exit(1)
            value = config.get(section, option)
            if option in ['border_width']:
                value = int(value)
            setattr(self.display, option, value)

    ############################################################################

    def parse_colors(self, config):

        self.colors = WmConfigColors()

        section = 'Colors'

        if section not in config.sections():
            return

        for option in config.options(section):
            if not hasattr(self.colors, option):
                print "Unknown color '%s' in '%s' section" % (option, section)
                sys.exit(1)
            setattr(self.colors, option, config.get(section, option))

    ############################################################################

    def parse_fonts(self, config):

        self.fonts = WmConfigFonts()

        section = 'Fonts'

        if section not in config.sections():
            return

        for option in config.options(section):
            if not hasattr(self.fonts, option):
                print "Unknown font '%s' in '%s' section" % (option, section)
                sys.exit(1)
            setattr(self.fonts, option, config.get(section, option))

    ############################################################################

    def parse_keys(self, display, config):

        section = 'Keys'

        if section not in config.sections():
            return

        commands = ['next_window',
                    'prev_window',
                    'kill_window']

        # TODO Handle multiple modifiers

        for key_def in config.options(section):

            (modifier, key) = key_def.split('+')

            if modifier == 'mod4':
                mod_mask = X.Mod4Mask
            elif modifier == 'mod3':
                mod_mask = X.Mod3Mask
            elif modifier == 'mod2':
                mod_mask = X.Mod2Mask
            elif modifier == 'mod1':
                mod_mask = X.Mod1Mask
            else:
                print "%s?" % (modifier)
                sys.exit(1)

            cmd = config.get(section, key_def)
            if cmd not in commands:
                print "Unknown command '%s' in '%s' section" % (cmd, section)
                sys.exit(1)

            keycode = display.keysym_to_keycode(XK.string_to_keysym(key))
            self.keys[(mod_mask, keycode)] = cmd
