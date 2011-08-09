# WmDisplay.py

import sys
import logging
import Xlib.display as Xdisplay
import Xlib.error as Xerror
import Xlib.X as X
from WmConfig import WmConfig
from WmScreen import WmScreen

class WmDisplay(object):

    def __init__(self, display_name):

        self.setup_display(display_name)
        self.config = WmConfig(self.display)
        self.setup_screens()
        self.set_active_screen(0)

    ############################################################################

    def setup_display(self, display_name):

        try:
            self.display = Xdisplay.Display(display_name)
        except Xerror.DisplayNameError:
            logging.critical("Display name '%s' is malformed", display_name)
            sys.exit(1)
        except Xerror.DisplayConnectionError:
            logging.critical("Connection to X server on display '%s' failed", display_name)
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

    def set_active_screen(self, screen_num):

        logging.debug("Setting screen %d active", screen_num)
        self.active_screen = 0

    ############################################################################

    def run_event_loop(self):
        while 1:
            event = self.display.next_event()

            if event.type in [X.KeyPress,
                              X.MapRequest,
                              X.ConfigureRequest,
                              X.UnmapNotify,
                              X.DestroyNotify]:
                self.screens[self.active_screen].handle_event(event)
                continue

            # TODO Do anything with these?

            if event.type == X.CirculateRequest:
                logging.debug("CirculateRequest: %s", event.window.get_wm_name())
                continue

            if event.type == X.ClientMessage:
                logging.debug("ClientMessage: %s", event.window.get_wm_name())
                continue

            # TODO This is a screen thing (I think)

            if event.type == X.EnterNotify:
                logging.debug("EnterNotify")
                continue
