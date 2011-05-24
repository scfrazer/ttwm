# WmScreen.py

import Xlib.X
import Xlib.error
import Xlib.XK
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

        # TODO

        release_mod = Xlib.X.AnyModifier << 1
        self.code = self.display.keysym_to_keycode(Xlib.XK.XK_h)
        print self.code

        self.root.grab_key(self.code,
                           Xlib.X.Mod4Mask & ~release_mod,
                           1,
                           Xlib.X.GrabModeAsync,
                           Xlib.X.GrabModeAsync)

        # Setup

        self.width = screen.width_in_pixels
        self.height = screen.height_in_pixels
        self.config = config

    def handle_key_press(self, event):
        if event.state & Xlib.X.Mod4Mask and event.detail == self.code:
            print "Got it"
