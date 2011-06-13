# WmScreen.py

import sys
import logging
import Xlib.X as X
import Xlib.error as Xerror
from WmData import WmData
from WmGroup import WmGroup

class WmScreen(object):

    def __init__(self, display, screen, config):

        self.become_wm(display, screen.root)
        self.wm_data = WmData(display, screen, config)

        self.grab_keys()

        self.claim_all_windows()

        group_name = 'Default'
        self.groups = {group_name: WmGroup(self.wm_data)}
        self.set_active_group(group_name)
        self.add_windows(self.windows)

    ############################################################################

    def become_wm(self, display, root):

        catch = Xerror.CatchError(Xerror.BadAccess)
        root.change_attributes(event_mask=X.SubstructureRedirectMask, onerror=catch)
        display.sync()
        if catch.get_error():
            logging.critical("Another window manager is already runing")
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

    def set_active_group(self, name):

        logging.debug("Setting group '%s' active", name)
        self.active_group = name

    ############################################################################

    def add_windows(self, windows):

        self.groups[self.active_group].add_windows(self.windows)

    ############################################################################

    def handle_key_press(self, event):

        lookup = (event.state, event.detail)
        if lookup in self.wm_data.config.keys:

            cmd = self.wm_data.config.keys[lookup]

            if cmd in ['next_window', 'prev_window']:
                self.groups[self.active_group].do_cmd(cmd)
                return True

        return False
