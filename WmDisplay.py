# WmDisplay.py

import Xlib.display as Xdisplay
import Xlib.error as Xerror
import Xlib.X as X
import sys
from WmConfig import WmConfig
from WmScreen import WmScreen

class WmDisplay(object):

    def __init__(self, display_name):

        self.setup_display(display_name)
        self.config = WmConfig(self.display)
        self.setup_screens()

    ############################################################################

    def setup_display(self, display_name):

        try:
            self.display = Xdisplay.Display(display_name)
        except Xerror.DisplayNameError:
            print "Display name '%s' is malformed" % (display_name)
            sys.exit(1)
        except Xerror.DisplayConnectionError:
            print "Connection to X server on display '%s' failed" % (display_name)
            sys.exit(1)

    ############################################################################

    def setup_screens(self):

        self.screens = []
        num_screens = self.display.screen_count()
        for screen_num in xrange(num_screens):
            self.screens.append(WmScreen(self.display,
                                         self.display.screen(screen_num),
                                         self.config))

    ############################################################################

    def run_event_loop(self):
        while 1:
            event = self.display.next_event()
            # TODO
            if event.type == X.KeyPress:
                for screen in self.screens:
                    if screen.handle_key_press(event):
                        break
