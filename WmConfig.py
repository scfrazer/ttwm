# WmConfig.py

import sys
import logging
import ConfigParser
import Xlib.X as X
import Xlib.XK as XK

################################################################################

class WmConfigObject(object):

    def __init__(self, display):
        self.display = display

    def parse(self, config_obj, section):

        if section not in config_obj.sections():
            return

        for option in config_obj.options(section):
            if not hasattr(self, option):
                print "Unknown option '%s' in '%s' section" % (option, section)
                sys.exit(1)
            setattr(self, option, config_obj.get(section, option))

        self.init_after_parse()

    def init_after_parse(self):
        pass

################################################################################

class WmConfigStack(WmConfigObject):

    def __init__(self, display):

        super(WmConfigStack, self).__init__(display)
        self.border_width = 1

    def init_after_parse(self):

        super(WmConfigStack, self).init_after_parse()
        self.border_width = int(self.border_width)

################################################################################

class WmConfigTab(WmConfigObject):

    def __init__(self, display):

        super(WmConfigTab, self).__init__(display)

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

    def init_after_parse(self):

        super(WmConfigTab, self).init_after_parse()

        self.border_width = int(self.border_width)
        self.padding = int(self.padding)

        colormap = self.display.screen(0).default_colormap

        self.ff_fg = colormap.alloc_named_color(self.ff_fg).pixel
        self.ff_bg = colormap.alloc_named_color(self.ff_bg).pixel
        self.ff_bo = colormap.alloc_named_color(self.ff_bo).pixel

        self.fu_fg = colormap.alloc_named_color(self.fu_fg).pixel
        self.fu_bg = colormap.alloc_named_color(self.fu_bg).pixel
        self.fu_bo = colormap.alloc_named_color(self.fu_bo).pixel

        self.uf_fg = colormap.alloc_named_color(self.uf_fg).pixel
        self.uf_bg = colormap.alloc_named_color(self.uf_bg).pixel
        self.uf_bo = colormap.alloc_named_color(self.uf_bo).pixel

        self.uu_fg = colormap.alloc_named_color(self.uu_fg).pixel
        self.uu_bg = colormap.alloc_named_color(self.uu_bg).pixel
        self.uu_bo = colormap.alloc_named_color(self.uu_bo).pixel

################################################################################

class WmConfigStatusBar(WmConfigObject):

    def __init__(self, display):

        super(WmConfigStatusBar, self).__init__(display)
        self.border_width = 1

        self.bg = '#607080'
        self.bo = '#607080'

    def init_after_parse(self):

        super(WmConfigStatusBar, self).init_after_parse()
        self.border_width = int(self.border_width)

        colormap = self.display.screen(0).default_colormap

        self.bg = colormap.alloc_named_color(self.bg).pixel
        self.bo = colormap.alloc_named_color(self.bo).pixel

################################################################################

class WmConfigGroup(WmConfigObject):

    def __init__(self, display):

        super(WmConfigGroup, self).__init__(display)

        self.font = '-*-helvetica-medium-r-*-*-14-*'
        self.border_width = 1
        self.padding = 1

        self.active_fg = '#ffffff'
        self.active_bg = '#607080'
        self.active_bo = '#708090'

        self.inactive_fg = '#a0a0a0'
        self.inactive_bg = '#405060'
        self.inactive_bo = '#607080'

    def init_after_parse(self):

        super(WmConfigGroup, self).init_after_parse()

        self.border_width = int(self.border_width)
        self.padding = int(self.padding)

        colormap = self.display.screen(0).default_colormap

        self.active_fg = colormap.alloc_named_color(self.active_fg).pixel
        self.active_bg = colormap.alloc_named_color(self.active_bg).pixel
        self.active_bo = colormap.alloc_named_color(self.active_bo).pixel

        self.inactive_fg = colormap.alloc_named_color(self.inactive_fg).pixel
        self.inactive_bg = colormap.alloc_named_color(self.inactive_bg).pixel
        self.inactive_bo = colormap.alloc_named_color(self.inactive_bo).pixel

################################################################################

class WmConfigMeter(WmConfigObject):

    def __init__(self, display):

        super(WmConfigMeter, self).__init__(display)

        self.font = '-*-helvetica-medium-r-*-*-14-*'
        self.border_width = 1
        self.padding = 1

        self.fg = '#ffffff'
        self.bg = '#607080'
        self.bo = '#708090'

    def init_after_parse(self):

        super(WmConfigMeter, self).init_after_parse()

        self.border_width = int(self.border_width)
        self.padding = int(self.padding)

        colormap = self.display.screen(0).default_colormap

        self.fg = colormap.alloc_named_color(self.fg).pixel
        self.bg = colormap.alloc_named_color(self.bg).pixel
        self.bo = colormap.alloc_named_color(self.bo).pixel

################################################################################

class WmConfig(object):

    def __init__(self, display):

        config_obj = self.read_config_file()

        self.stack = WmConfigStack(display)
        self.stack.parse(config_obj, "Stack")

        self.tab = WmConfigTab(display)
        self.tab.parse(config_obj, "Tab")

        self.status_bar = WmConfigStatusBar(display)
        self.status_bar.parse(config_obj, "StatusBar")

        self.group = WmConfigGroup(display)
        self.group.parse(config_obj, "Group")

        self.meter = WmConfigMeter(display)
        self.meter.parse(config_obj, "Meter")

        self.keys = {}
        self.parse_keys(display, config_obj)

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
