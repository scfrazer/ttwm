# WmScreen.py

import sys
import logging
import Xlib.X as X
import Xlib.error as Xerror
import Xlib.Xutil as Xutil
from WmData import WmData
from WmGroup import WmGroup

class WmScreen(object):

    def __init__(self, display, screen, config):

        self.become_wm(display, screen.root)
        self.wm_data = WmData(display, screen, config)
        self.grab_keys()

        self.event_dispatch = {
            X.KeyPress: self.event_key_press,
            X.MapRequest: self.event_map_request,
            X.UnmapNotify: self.event_unmap_notify,
            X.DestroyNotify: self.event_destroy_notify
            }

        self.cmd_dispatch = {}

        self.create_status_bar()

        self.groups = {}
        self.add_group('Default')

        self.windows = []
        self.claim_all_windows()

    ############################################################################

    def become_wm(self, display, root):

        catch = Xerror.CatchError(Xerror.BadAccess)
        root.change_attributes(event_mask=(X.SubstructureRedirectMask
                                           | X.SubstructureNotifyMask),
                               onerror=catch)
        display.sync()
        if catch.get_error():
            logging.critical("Another window manager is already running")
            sys.exit(1)

    ############################################################################

    def grab_keys(self):

        release_mod = X.AnyModifier << 1
        for item in self.wm_data.keymap:
            (mod_mask, keycode) = item
            self.wm_data.root.grab_key(keycode, mod_mask & ~release_mod,
                                       1, X.GrabModeAsync, X.GrabModeAsync)

    ############################################################################

    def create_status_bar(self):
        # TODO
        pass

    ############################################################################

    def add_group(self, name):

        logging.debug("Adding group '%s'", name)
        if name in self.groups:
            logging.error("Group '%s' already exists, ignoring command", name)
            return
        self.groups = {name: WmGroup(self.wm_data)}
        self.set_active_group(name)

    ############################################################################

    def set_active_group(self, name):

        logging.debug("Setting group '%s' active", name)
        self.active_group = name
        self.update_status_bar()

    ############################################################################

    def claim_all_windows(self):

        windows = self.wm_data.root.query_tree().children
        for window in windows:

            if not window.get_wm_name():
                continue

            wm_state = window.get_wm_state()
            if wm_state == Xutil.WithdrawnState:
                continue

            wm_hints = window.get_wm_hints()
            if wm_hints and wm_hints.flags & Xutil.IconWindowHint:
                continue

            attrs = window.get_attributes()
            if attrs.override_redirect or attrs.map_state == X.IsUnmapped:
                continue

            self.windows.append(window)
            window.change_save_set(X.SetModeInsert)

            self.groups[self.active_group].add_window(window)

    ############################################################################

    def update_status_bar(self):
        # TODO
        pass

    ############################################################################

    def handle_event(self, event):

        if event.type in self.event_dispatch:
            self.event_dispatch[event.type](event)
        else:
            self.groups[self.active_group].handle_event(event)

    ############################################################################

    def event_key_press(self, event):

        lookup = (event.state, event.detail)
        if lookup in self.wm_data.keymap:

            cmd = self.wm_data.keymap[lookup]
            if cmd in self.cmd_dispatch:
                self.cmd_dispatch[cmd]()
            else:
                self.groups[self.active_group].do_cmd(cmd)

    ############################################################################

    def event_map_request(self, event):

        event.window.map()

        if event.window not in self.windows:
            self.windows.append(event.window)
            event.window.change_save_set(X.SetModeInsert)
            self.groups[self.active_group].handle_event(event)

    ############################################################################

    def event_unmap_notify(self, event):

        if event.window in self.windows:
            logging.debug("UnmapNotify for window %s", event.window)

    ############################################################################

    def event_destroy_notify(self, event):

        if event.window in self.windows:
            logging.debug("DestroyNotify for window %s", event.window)
            event.window.change_save_set(X.SetModeDelete)
            for group_name in self.groups:
                self.groups[group_name].remove_window(event.window)
            self.windows.remove(event.window)
