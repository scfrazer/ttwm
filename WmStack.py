# WmStack.py

import logging
import Xlib.X as X

class WmStack(object):

    def __init__(self, wm_data, top, left, width, height):

        self.wm_data = wm_data

        self.event_dispatch = {
            X.MapRequest: self.event_map_request,
            X.ConfigureRequest: self.event_configure_request
            }

        self.cmd_dispatch = {
            'next_window': self.cmd_next_window,
            'prev_window': self.cmd_prev_window,
            'kill_window': self.cmd_kill_window
            }

        border_width = self.wm_data.config.display.border_width
        self.top = top
        self.left = left
        self.width = width - 2 * border_width
        self.height = height - 2 * border_width
        self.y_offset = self.wm_data.config.display.tab_height - 1  # -1 to match tabs

        self.left_windows = []
        self.tab_windows = []
        self.right_windows = []

        self.create_parent_window()
        self.parent_window.map()

        self.tabs = []
        self.top_tab_num = 0  # This is an index into self.tabbed_windows
        self.draw_tabs()

    ############################################################################

    def create_parent_window(self):

        self.parent_window = self.wm_data.root.create_window(
            self.top, self.left, self.width, self.height,
            self.wm_data.config.display.border_width,
            X.CopyFromParent, X.InputOutput, X.CopyFromParent,
            border_pixel=self.wm_data.config.colors.tab_ff_bg)

        self.parent_window.change_attributes(event_mask=X.SubstructureNotifyMask)

    ############################################################################

    def draw_tabs(self):

        for tab in self.tabs:
            tab.unmap()
            tab.destroy()

        if len(self.tab_windows) == 0:
            return

        tab_width = self.width / len(self.tab_windows)
        tab_width_leftover = self.width % len(self.tab_windows)

        # TODO Limit number of tabs

        self.tabs = []
        left_edge = 0
        for (tab_num, window) in enumerate(self.tab_windows):

            width = tab_width
            if tab_num < tab_width_leftover:
                width += 1

            tab = self.parent_window.create_window(
                left_edge, -1,  # -1 so it's flush with the parent border
                width - 2, self.wm_data.config.display.tab_height - 2,  # -2 for border
                1, X.CopyFromParent, X.InputOutput, X.CopyFromParent)

            left_edge += width

            tab.map()
            self.tabs.append(tab)
            self.update_tab(tab_num)

    ############################################################################

    def update_tab(self, tab_num):

        # TODO Unfocused tabs

        if tab_num == self.top_tab_num:
            gc = self.wm_data.gcs.tab_ff
            background_pixel = self.wm_data.config.colors.tab_ff_bg
            border_pixel = self.wm_data.config.colors.tab_ff_bo
        else:
            gc = self.wm_data.gcs.tab_fu
            background_pixel = self.wm_data.config.colors.tab_fu_bg
            border_pixel = self.wm_data.config.colors.tab_fu_bo

        tab = self.tabs[tab_num]
        tab.change_attributes(border_pixel=border_pixel,
                              background_pixel=background_pixel)

        geom = tab.get_geometry()
        title_text = self.tab_windows[tab_num].get_wm_name()
        title_text_extents = gc.query_text_extents(title_text)
        tab.clear_area(width=geom.width, height=geom.height)
        tab.draw_text(gc, (geom.width - title_text_extents.overall_width) / 2,
                      self.wm_data.config.fonts.title_height - 2,  # -2 for border
                      title_text)

    ############################################################################

    def add_window(self, window):

        # TODO Limit number of tabs

        logging.debug("Adding window '%s' %s", window.get_wm_name(), window)

        # Turn off SubstructureNotifyMask during reparent to avoid spurious
        # UnmapNotify

        self.wm_data.root.change_attributes(event_mask=X.SubstructureRedirectMask)
        window.reparent(self.parent_window, 0, self.y_offset)
        self.wm_data.root.change_attributes(event_mask=(X.SubstructureRedirectMask
                                                        | X.SubstructureNotifyMask))
        self.resize_window(window)

        if len(self.tab_windows) == 0:
            self.top_tab_num = 0
            self.tab_windows.append(window)
        else:
            self.top_tab_num += 1
            self.tab_windows.insert(self.top_tab_num, window)

        self.draw_tabs()

    ############################################################################

    def remove_window(self, window):

        # TODO Look in left/right windows too

        window_idx = self.tab_windows.index(window)
        if window_idx is not None:

            logging.debug("Removing window %s", window)

            if self.top_tab_num == window_idx:
                self.top_tab_num -= 1
                if self.top_tab_num < 0:
                    self.top_tab_num = 0

            del self.tab_windows[window_idx]
            self.draw_tabs()

    ############################################################################

    def resize_window(self, window):
        window.configure(width=self.width, height=self.height - self.y_offset)

    ############################################################################

    def handle_event(self, event):

        if event.type in self.event_dispatch:
            self.event_dispatch[event.type](event)

    ############################################################################

    def event_map_request(self, event):
        self.add_window(event.window)

    ############################################################################

    def event_configure_request(self, event):
        self.resize_window(event.window)

    ############################################################################

    def do_cmd(self, cmd):

        if cmd in self.cmd_dispatch:
            self.cmd_dispatch[cmd]()

    ############################################################################

    def cmd_next_window(self):

        if len(self.tab_windows) < 2:
            return

        # TODO Handle extra left/right tabs

        old_top_tab_num = self.top_tab_num
        self.top_tab_num += 1
        if self.top_tab_num >= len(self.tab_windows):
            self.top_tab_num = 0

        self.update_tab(old_top_tab_num)
        self.update_tab(self.top_tab_num)
        self.tab_windows[self.top_tab_num].configure(stack_mode=X.Above)

    ############################################################################

    def cmd_prev_window(self):

        if len(self.tab_windows) < 2:
            return

        # TODO Handle extra left/right tabs

        old_top_tab_num = self.top_tab_num
        self.top_tab_num -= 1
        if self.top_tab_num < 0:
            self.top_tab_num = len(self.tab_windows) - 1

        self.update_tab(old_top_tab_num)
        self.update_tab(self.top_tab_num)
        self.tab_windows[self.top_tab_num].configure(stack_mode=X.Above)

    ############################################################################

    def cmd_kill_window(self):
        pass
