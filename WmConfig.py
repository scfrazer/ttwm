# WmConfig.py

import sys
import logging
import ConfigParser
import Xlib.X as X
import Xlib.XK as XK

class WmConfig(object):

    ############################################################################

    def __init__(self, display):

        config = self.read_config_file()

        # Display

        self.display = {}
        self.display['border_width'] = 1

        self.parse_display(config)

        # Colors

        self.colors = {}

        self.colors['focus_top_fg'] = '#ffffff'
        self.colors['focus_top_bg'] = '#607080'
        self.colors['focus_top_bo'] = '#708090'

        self.colors['focus_und_fg'] = '#a0a0a0'
        self.colors['focus_und_bg'] = '#405060'
        self.colors['focus_und_bo'] = '#607080'

        self.colors['unfocus_top_fg'] = '#c0c0c0'
        self.colors['unfocus_top_bg'] = '#405060'
        self.colors['unfocus_top_bo'] = '#607080'

        self.colors['unfocus_und_fg'] = '#a0a0a0'
        self.colors['unfocus_und_bg'] = '#304050'
        self.colors['unfocus_und_bo'] = '#506070'

        self.parse_colors(config)

        # Fonts

        self.fonts = {}
        self.fonts['title'] = '-*-helvetica-medium-r-*-*-12-*'

        self.parse_fonts(config)

        # Keys

        self.keys = {}
        self.commands = ['next_window',
                         'prev_window',
                         'kill_window']

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

        section = 'Display'

        if section not in config.sections():
            return

        for option in config.options(section):
            if option not in self.display:
                print "Unknown option '%s' in '%s' section" % (option, section)
                sys.exit(1)
            value = config.get(section, option)
            if option in ['border_width']:
                self.display[option] = int(value)
            else:
                self.display[option] = value

    ############################################################################

    def parse_colors(self, config):

        section = 'Colors'

        if section not in config.sections():
            return

        for option in config.options(section):
            if option not in self.colors:
                print "Unknown color '%s' in '%s' section" % (option, section)
                sys.exit(1)
            value = config.get(section, option)
            self.colors[option] = value

    ############################################################################

    def parse_fonts(self, config):

        section = 'Fonts'

        if section not in config.sections():
            return

        for option in config.options(section):
            if option not in self.fonts:
                print "Unknown font '%s' in '%s' section" % (option, section)
                sys.exit(1)
            value = config.get(section, option)
            self.fonts[option] = value

    ############################################################################

    def parse_keys(self, display, config):

        section = 'Keys'

        if section not in config.sections():
            return

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
            if cmd not in self.commands:
                print "Unknown command '%s' in '%s' section" % (cmd, section)
                sys.exit(1)

            keycode = display.keysym_to_keycode(XK.string_to_keysym(key))
            self.keys[(mod_mask, keycode)] = cmd
