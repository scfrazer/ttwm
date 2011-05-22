# WmDisplay.py

from Xlib.display import Display
import Xlib.error
import sys
from WmConfig import WmConfig
from WmScreen import WmScreen

class WmDisplay(object):

    def __init__(self, display_name):

        try:
            self.display = Display(display_name)
        except Xlib.error.DisplayNameError:
            print "Display name '%s' is malformed" % (display_name)
            sys.exit(1)
        except Xlib.error.DisplayConnectionError:
            print "Connection to X server for display '%s' failed" % (display_name)
            sys.exit(1)

        self.screens = []

    def run_event_loop(self):
        pass
