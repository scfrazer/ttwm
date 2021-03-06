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
            X.DestroyNotify: self.event_destroy_notify,
            X.ClientMessage: self.event_client_message
            }

        self.cmd_dispatch = {}

        self.create_status_bar()

        self.groups = []
        self.focused_group_num = 0
        self.add_group('Default')

        self.windows = []
        self.claim_all_windows()

        self.draw_group_tabs()

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

        geom = self.wm_data.root.get_geometry()

        x = 0
        y = geom.height - self.wm_data.status_bar.height
        width = geom.width - 2 * self.wm_data.status_bar.border_width
        height = self.wm_data.status_bar.height - 2 * self.wm_data.status_bar.border_width

        self.status_bar_window = self.wm_data.root.create_window(
            x, y, width, height, self.wm_data.status_bar.border_width,
            X.CopyFromParent, X.InputOutput, X.CopyFromParent,
            background_pixel=self.wm_data.status_bar.bg,
            border_pixel=self.wm_data.status_bar.bo)

        self.status_bar_window.change_attributes(event_mask=X.SubstructureNotifyMask)
        self.status_bar_window.map()

    ############################################################################

    def add_group(self, name):

        logging.debug("Adding group '%s'", name)
        if self.groups:
            self.focused_group_num += 1
        self.groups.insert(self.focused_group_num, WmGroup(name, self.wm_data))

        self.draw_group_tabs()
        self.focus_group_num(self.focused_group_num)

    ############################################################################

    def draw_group_tabs(self):

        for group in self.groups:
            if group.tab:
                group.tab.unmap()
                group.tab.destroy()

        geom = self.wm_data.root.get_geometry()
        self.status_bar_window.clear_area(0, 0, geom.width, self.wm_data.status_bar.height)

        left_edge = 0
        for (group_num, group) in enumerate(self.groups):

            if group_num == self.focused_group_num:
                gc = self.wm_data.group.f_gc
            else:
                gc = self.wm_data.group.u_gc

            text = self.groups[group_num].name
            text_extents = gc.query_text_extents(text + " (00)")
            total_width = (text_extents.overall_width
                           + 2 * self.wm_data.group.padding
                           + 2 * self.wm_data.group.border_width)

            x = left_edge
            y = 0
            width = total_width - 2 * self.wm_data.tab.border_width
            height = self.wm_data.group.height - 2 * self.wm_data.group.border_width

            tab = self.status_bar_window.create_window(
                x, y, width, height, self.wm_data.tab.border_width,
                X.CopyFromParent, X.InputOutput, X.CopyFromParent)

            left_edge += total_width

            tab.map()
            group.tab = tab
            self.update_group_tab(group_num)

    ############################################################################

    def update_group_tab(self, group_num):

        if group_num == self.focused_group_num:
            gc = self.wm_data.group.f_gc
            bg = self.wm_data.group.f_bg
            bo = self.wm_data.group.f_bo
        else:
            gc = self.wm_data.group.u_gc
            bg = self.wm_data.group.u_bg
            bo = self.wm_data.group.u_bo

        tab = self.groups[group_num].tab
        tab.change_attributes(border_pixel=bo, background_pixel=bg)

        geom = tab.get_geometry()
        title_text = "%s (%d)" % (self.groups[group_num].name, self.groups[group_num].num_windows())
        title_text_extents = gc.query_text_extents(title_text)
        tab.clear_area(width=geom.width, height=geom.height)
        tab.draw_text(gc, (geom.width - title_text_extents.overall_width) / 2,
                      self.wm_data.group.font_y_offset, title_text)

    ############################################################################

    def focus_group_num(self, group_num):

        logging.debug("Focusing group %d ('%s')", group_num, self.groups[group_num].name)
        # TODO Change groups
        self.focused_group_num = group_num

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

            top_window = window.get_wm_transient_for()
            if top_window:
                for group in self.groups:
                    group.add_transient(top_window, window)
            else:
                self.groups[self.focused_group_num].add_window(window)

    ############################################################################

    def handle_event(self, event):

        if event.type in self.event_dispatch:
            self.event_dispatch[event.type](event)
        else:
            self.groups[self.focused_group_num].handle_event(event)

    ############################################################################

    def event_key_press(self, event):

        lookup = (event.state, event.detail)
        if lookup in self.wm_data.keymap:

            cmd = self.wm_data.keymap[lookup]
            if cmd in self.cmd_dispatch:
                logging.debug(cmd)
                self.cmd_dispatch[cmd]()
            else:
                self.groups[self.focused_group_num].do_cmd(cmd)

    ############################################################################

    def event_map_request(self, event):

        window = event.window
        logging.debug("MapNotify for window %s", window)
        window.map()

        top_window = window.get_wm_transient_for()
        if top_window:
            for group in self.groups:
                group.add_transient(top_window, window)
        elif window not in self.windows:
            self.windows.append(window)
            window.change_save_set(X.SetModeInsert)
            self.groups[self.focused_group_num].handle_event(event)
            self.update_group_tab(self.focused_group_num)

    ############################################################################

    def event_unmap_notify(self, event):

        if event.window in self.windows:
            logging.debug("UnmapNotify for window %s", event.window)

    ############################################################################

    def event_destroy_notify(self, event):

        if event.window in self.windows:
            logging.debug("DestroyNotify for window %s", event.window)
            for group in self.groups:
                group.remove_window(event.window)
            self.windows.remove(event.window)
            self.update_group_tab(self.focused_group_num)

    ############################################################################

    def event_client_message(self, event):

        if event.client_type == wm_data.atoms._NET_ACTIVE_WINDOW:
            print "TODO: _NET_ACTIVE_WINDOW"
        else:
            logging.warning("ClientMessage: %s from %s", self.display.get_atom_name(event.client_type), event.window)
