# WmConfig.py

import sys
import logging
import types
import ConfigParser

################################################################################

class WmConfigObject(object):

    def parse(self, config_obj, section):

        if section not in config_obj.sections():
            return

        for option in config_obj.options(section):

            if not hasattr(self, option):
                print "Unknown option '%s' in '%s' section" % (option, section)
                sys.exit(1)

            if type(getattr(self, option)) == types.IntType:
                setattr(self, option, int(config_obj.get(section, option)))
            else:
                setattr(self, option, config_obj.get(section, option))

################################################################################

class WmConfigStack(WmConfigObject):

    def __init__(self, config_obj, section):

        self.border_width = 1

        self.parse(config_obj, section)

################################################################################

class WmConfigTab(WmConfigObject):

    def __init__(self, config_obj, section):

        self.font = '-*-helvetica-medium-r-*-*-12-*'
        self.border_width = 1
        self.padding = 1

        self.ff_fg = '#ffffff'
        self.ff_bg = '#607080'
        self.ff_bo = '#708090'

        self.fu_fg = '#a0a0a0'
        self.fu_bg = '#405060'
        self.fu_bo = '#607080'

        self.uf_fg = '#c0c0c0'
        self.uf_bg = '#405060'
        self.uf_bo = '#607080'

        self.uu_fg = '#a0a0a0'
        self.uu_bg = '#304050'
        self.uu_bo = '#506070'

        self.parse(config_obj, section)

################################################################################

class WmConfigStatusBar(WmConfigObject):

    def __init__(self, config_obj, section):

        self.border_width = 1

        self.bg = '#607080'
        self.bo = '#607080'

        self.parse(config_obj, section)

################################################################################

class WmConfigGroup(WmConfigObject):

    def __init__(self, config_obj, section):

        self.font = '-*-helvetica-medium-r-*-*-14-*'
        self.border_width = 1
        self.padding = 1

        self.f_fg = '#ffffff'
        self.f_bg = '#607080'
        self.f_bo = '#708090'

        self.u_fg = '#a0a0a0'
        self.u_bg = '#405060'
        self.u_bo = '#607080'

        self.parse(config_obj, section)

################################################################################

class WmConfigMeter(WmConfigObject):

    def __init__(self, config_obj, section):

        self.font = '-*-helvetica-medium-r-*-*-14-*'
        self.border_width = 1
        self.padding = 1

        self.fg = '#ffffff'
        self.bg = '#607080'
        self.bo = '#607080'

        self.parse(config_obj, section)

################################################################################

class WmConfigKeys(WmConfigObject):

    def __init__(self, config_obj, section):

        self.next_window = "Mod4+n"
        self.prev_window = "Mod4+p"
        self.kill_window = "Mod4+q"

        self.parse(config_obj, section)

################################################################################

class WmConfig(object):

    def __init__(self):

        config_obj = self.read_config_file()

        self.stack = WmConfigStack(config_obj, "Stack")
        self.tab = WmConfigTab(config_obj, "Tab")
        self.status_bar = WmConfigStatusBar(config_obj, "StatusBar")
        self.group = WmConfigGroup(config_obj, "Group")
        self.meter = WmConfigMeter(config_obj, "Meter")
        self.keys = WmConfigKeys(config_obj, "Keys")

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
