# WmScreen.py

import Xlib.X
import Xlib.error
import sys

class WmScreen(object):

    def __init__(self, display, screen, config):

        self.display = display

        # Get root access

        self.root = screen.root
        catch = Xlib.error.CatchError(Xlib.error.BadAccess)
        self.root.change_attributes(event_mask=(Xlib.X.EnterWindowMask
                                                | Xlib.X.LeaveWindowMask
                                                | Xlib.X.PropertyChangeMask
                                                | Xlib.X.FocusChangeMask
                                                | Xlib.X.SubstructureRedirectMask
                                                | Xlib.X.SubstructureNotifyMask),
                                    onerror=catch)
        self.display.sync()
        if catch.get_error():
            print "Another window manager is already runing"
            sys.exit(1)

        # Setup

        self.width = screen.width_in_pixels
        self.height = screen.height_in_pixels
        self.config = config
