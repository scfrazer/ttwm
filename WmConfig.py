# WmConfig.py

import sys
import ConfigParser
import Xlib.X
import Xlib.XK

class WmConfig(object):

    ############################################################################

    def __init__(self, display):

        config = self.read_config_file()

        # Display options

        self.display_opts = {}
        self.display_opts['border_width'] = 1
        self.display_opts['focused_color'] = 'DodgerBlue1'
        self.display_opts['other_focused_color'] = 'DarkBlue'
        self.display_opts['unfocused_color'] = 'Gray'

        self.parse_display_options(config)

        # Keys

        self.keymap = {}
        self.commands = ['split_horizontal',
                         'split_vertical',
                         'next_stack',
                         'prev_stack',
                         'kill_stack']

        self.parse_key_defs(display, config)

    ############################################################################

    def read_config_file(self):

        filename = '.ttwmrc'  # TODO Find this in various places

        try:
            config_file = open(filename)
        except IOError:
            print "\nError: Couldn't read '%s'\n" % (filename)
            return

        config = ConfigParser.RawConfigParser()
        config.readfp(config_file)
        config_file.close()

        return config

    ############################################################################

    def parse_display_options(self, config):

        section = 'Display'

        if section not in config.sections():
            return

        for option in config.options(section):
            if option not in self.display_opts:
                print "Unknown option '%s' in 'Display' section" % (option)
                sys.exit(1)
            value = config.get(section, option)
            if option in ['border_width']:
                self.display_opts[option] = int(value)
            else:
                self.display_opts[option] = value

    ############################################################################

    def parse_key_defs(self, display, config):

        section = 'Keys'

        if section not in config.sections():
            return

        for key_def in config.options(section):

            (modifier, key) = key_def.split('+')

            if modifier == 'mod4':
                mod_mask = Xlib.X.Mod4Mask
            elif modifier == 'mod3':
                mod_mask = Xlib.X.Mod3Mask
            elif modifier == 'mod2':
                mod_mask = Xlib.X.Mod2Mask
            elif modifier == 'mod1':
                mod_mask = Xlib.X.Mod1Mask
            else:
                print "%s?" % (modifier)
                sys.exit(1)

            cmd = config.get(section, key_def)
            if cmd not in self.commands:
                print "Unknown command '%s' in 'Keys' section" % (cmd)
                sys.exit(1)

            keycode = display.keysym_to_keycode(Xlib.XK.string_to_keysym(key))
            self.keymap[(mod_mask, keycode)] = cmd
