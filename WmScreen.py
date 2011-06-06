# WmScreen.py

import Xlib.X as X
import Xlib.error as Xerror
import sys
from WmData import WmData
from WmGroup import WmGroup

class WmScreen(object):

    def __init__(self, display, screen, config):

        self.become_wm(display, screen.root)
        self.wm_data = WmData(display, screen, config)

        self.grab_keys()

        self.claim_all_windows()

        self.groups = {'Default': WmGroup(self.wm_data)}
        self.groups['Default'].add_windows(self.windows)

    ############################################################################

    def become_wm(self, display, root):

        catch = Xerror.CatchError(Xerror.BadAccess)
        root.change_attributes(event_mask=(X.PropertyChangeMask
                                           | X.FocusChangeMask
                                           | X.SubstructureRedirectMask
                                           | X.SubstructureNotifyMask),
                               onerror=catch)
        display.sync()
        if catch.get_error():
            print "Another window manager is already runing"
            sys.exit(1)

    ############################################################################

    def grab_keys(self):

        release_mod = X.AnyModifier << 1
        for item in self.wm_data.config.keys:
            (mod_mask, keycode) = item
            self.wm_data.root.grab_key(keycode, mod_mask & ~release_mod,
                                       1, X.GrabModeAsync, X.GrabModeAsync)

    ############################################################################

    def claim_all_windows(self):

        self.windows = []
        windows = self.wm_data.root.query_tree().children
        for window in windows:
            if not window.get_wm_name():
                continue
            attrs = window.get_attributes()
            if attrs.override_redirect or attrs.map_state == X.IsUnmapped:
                continue
            self.windows.append(window)
            window.change_save_set(X.SetModeInsert)

    ############################################################################

    def handle_key_press(self, event):
        lookup = (event.state, event.detail)
        # TODO
        if lookup in self.wm_data.config.keys:
            print self.wm_data.config.keys[lookup]
