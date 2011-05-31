# WmConfig.py

import sys
import ConfigParser
import Xlib.X as X
import Xlib.XK as XK

class WmConfig(object):

    ############################################################################

    def __init__(self, display):

        config = self.read_config_file()

        # Display options

        self.display_opts = {}
        self.display_opts['border_width'] = 1
        self.display_opts['active_selected_fg'] = '#ffffff'
        self.display_opts['active_selected_bg'] = '#708090'
        self.display_opts['active_unselected_fg'] = '#a0a0a0'
        self.display_opts['active_unselected_bg'] = '#607080'
        self.display_opts['inactive_selected_fg'] = '#c0c0c0'
        self.display_opts['inactive_selected_bg'] = '#607080'
        self.display_opts['inactive_unselected_fg'] = '#a0a0a0'
        self.display_opts['inactive_unselected_bg'] = '#506070'

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
                print "Unknown command '%s' in 'Keys' section" % (cmd)
                sys.exit(1)

            keycode = display.keysym_to_keycode(XK.string_to_keysym(key))
            self.keymap[(mod_mask, keycode)] = cmd
