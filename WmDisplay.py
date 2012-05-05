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
        self.config = WmConfig()
        self.setup_screens()
        self.focus_screen_num(0)

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

    def focus_screen_num(self, screen_num):

        logging.debug("Focusing screen %d", screen_num)
        # TODO Change screen focus
        self.focused_screen_num = screen_num

    ############################################################################

    def run_event_loop(self):
        while 1:
            event = self.display.next_event()

            if event.type in [X.KeyPress,
                              X.MapRequest]:
                self.screens[self.focused_screen_num].handle_event(event)
                continue

            elif event.type in [X.ConfigureRequest,
                                X.UnmapNotify,
                                X.DestroyNotify,
                                X.ClientMessage]:
                for screen in self.screens:
                    screen.handle_event(event)
                continue

            # TODO Do something with CirculateRequest?

            elif event.type == X.CirculateRequest:
                logging.warning("CirculateRequest: %s", event.window)
                continue

            # TODO Do something with EnterNotify (screen)?

            elif event.type == X.EnterNotify:
                logging.warning("EnterNotify")
                continue
