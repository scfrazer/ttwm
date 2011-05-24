# WmScreen.py

import Xlib.X
import Xlib.error
import Xlib.XK
import sys

class WmScreen(object):

    def __init__(self, display, screen, config):

        self.display = display
        self.config = config

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

        # Grab keys

        release_mod = Xlib.X.AnyModifier << 1
        for item in self.config.keymap:
            (mod_mask, keycode) = item
            self.root.grab_key(keycode, mod_mask & ~release_mod,
                               1, Xlib.X.GrabModeAsync, Xlib.X.GrabModeAsync)

        # Other setup

        self.width = screen.width_in_pixels
        self.height = screen.height_in_pixels

    def handle_key_press(self, event):
        lookup = (event.state, event.detail)
        if lookup in self.config.keymap:
            print self.config.keymap[lookup]
