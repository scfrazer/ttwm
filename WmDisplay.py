# WmDisplay.py

import Xlib.display
import Xlib.error
import sys
from WmConfig import WmConfig
from WmScreen import WmScreen

class WmDisplay(object):

    def __init__(self, display_name):

        try:
            self.display = Xlib.display.Display(display_name)
        except Xlib.error.DisplayNameError:
            print "Display name '%s' is malformed" % (display_name)
            sys.exit(1)
        except Xlib.error.DisplayConnectionError:
            print "Connection to X server on display '%s' failed" % (display_name)
            sys.exit(1)

        self.config = WmConfig()

        self.screens = []
        num_screens = self.display.screen_count()
        for screen_num in xrange(num_screens):
            self.screens.append(WmScreen(self.display,
                                         self.display.screen(screen_num),
                                         self.config))

    def run_event_loop(self):
        while 1:
            event = self.display.next_event()
