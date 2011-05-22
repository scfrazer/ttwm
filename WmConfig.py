# WmConfig.py

import sys
import ConfigParser

class WmConfig(object):

    def __init__(self, display):

        filename = '.ttwmrc'  # TODO Find this in various places

        try:
            config_file = open(filename)
        except IOError:
            print "\nError: Couldn't read '%s'\n" % (filename)
            return

        config = ConfigParser.RawConfigParser()
        config.readfp(config_file)
        config_file.close()

        self.display_map = {}
        self.display_map['edge_width'] = 2
        self.display_map['edge_gap'] = 4
        self.display_map['focused_edge_color'] = 'DodgerBlue1'
        self.display_map['unfocused_edge_color'] = 'Gray'

        for section in config.sections():

            if section == 'Display':
                for option in config.options('Display'):
                    if option not in self.display_map:
                        print "Unknown option '%s' in 'Display' section" % (option)
                        sys.exit(1)
                    value = config.get(section, option)
                    self.display_map[option] = value

            elif section == 'Keys':
                pass

            else:
                print "Unknown section '%s' in '%s'" % (section, filename)
                sys.exit(1)
