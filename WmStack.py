# WmStack.py

import logging
import Xlib.X as X
import Xlib.protocol as Xprotocol

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

        self.top = top
        self.left = left
        self.width = width - 2 * wm_data.stack.border_width
        self.height = height - 2 * wm_data.stack.border_width
        self.client_y_offset = wm_data.tab.height - wm_data.stack.border_width

        self.focused = True

        self.windows = []
        self.focused_window_num = 0

        self.create_parent_window()
        self.parent_window.map()

        self.tabs = []
        self.draw_tabs()

    ############################################################################

    def create_parent_window(self):

        self.parent_window = self.wm_data.root.create_window(
            self.left, self.top, self.width, self.height,
            self.wm_data.stack.border_width,
            X.CopyFromParent, X.InputOutput, X.CopyFromParent,
            background_pixmap=X.ParentRelative,
            border_pixel=self.wm_data.tab.ff_bg)

        self.parent_window.change_attributes(event_mask=X.SubstructureNotifyMask)

    ############################################################################

    def draw_tabs(self):

        for tab in self.tabs:
            tab.unmap()
            tab.destroy()

        if len(self.windows) == 0:
            self.parent_window.clear_area(0, 0, self.width, self.height)
            self.focused_window_num = 0
            return

        tab_width = self.width / len(self.windows)
        tab_width_leftover = self.width % len(self.windows)

        self.tabs = []
        left_edge = 0
        for (tab_num, window) in enumerate(self.windows):

            width = tab_width
            if tab_num < tab_width_leftover:
                width += 1

            tab = self.parent_window.create_window(
                left_edge,
                0 - self.wm_data.stack.border_width,
                width - 2 * self.wm_data.tab.border_width,
                self.wm_data.tab.height - 2 * self.wm_data.tab.border_width,
                self.wm_data.tab.border_width,
                X.CopyFromParent, X.InputOutput, X.CopyFromParent)

            left_edge += width

            tab.map()
            self.tabs.append(tab)
            self.update_tab(tab_num)

    ############################################################################

    def update_tab(self, tab_num):

        if self.focused:
            if tab_num == self.focused_window_num:
                gc = self.wm_data.tab.ff_gc
                bg = self.wm_data.tab.ff_bg
                bo = self.wm_data.tab.ff_bo
            else:
                gc = self.wm_data.tab.fu_gc
                bg = self.wm_data.tab.fu_bg
                bo = self.wm_data.tab.fu_bo
        else:
            if tab_num == self.focused_window_num:
                gc = self.wm_data.tab.uf_gc
                bg = self.wm_data.tab.uf_bg
                bo = self.wm_data.tab.uf_bo
            else:
                gc = self.wm_data.tab.uu_gc
                bg = self.wm_data.tab.uu_bg
                bo = self.wm_data.tab.uu_bo

        tab = self.tabs[tab_num]
        tab.change_attributes(border_pixel=bo, background_pixel=bg)

        geom = tab.get_geometry()
        title_text = self.windows[tab_num].get_wm_name()
        title_text_extents = gc.query_text_extents(title_text)
        tab.clear_area(width=geom.width, height=geom.height)
        tab.draw_text(gc, (geom.width - title_text_extents.overall_width) / 2,
                      self.wm_data.tab.font_y_offset, title_text)

    ############################################################################

    def add_window(self, window):

        logging.debug("Adding window '%s' %s", window.get_wm_name(), window)

        # Turn off SubstructureNotifyMask during reparent to avoid spurious
        # UnmapNotify

        self.wm_data.root.change_attributes(event_mask=X.SubstructureRedirectMask)
        window.reparent(self.parent_window, 0, self.client_y_offset)
        self.wm_data.root.change_attributes(event_mask=(X.SubstructureRedirectMask
                                                        | X.SubstructureNotifyMask))
        self.resize_window(window)

        if self.windows:
            self.focused_window_num += 1
        self.windows.insert(self.focused_window_num, window)

        self.draw_tabs()
        self.focus_window_num(self.focused_window_num)

    ############################################################################

    def focus_window_num(self, window_num):

        if window_num >= len(self.windows):
            return

        window = self.windows[window_num]
        window.configure(stack_mode=X.Above)
        window.set_input_focus(X.RevertToPointerRoot, X.CurrentTime)

        if window_num != self.focused_window_num:
            old_focused_window_num = self.focused_window_num
            self.focused_window_num = window_num
            self.update_tab(old_focused_window_num)
            self.update_tab(self.focused_window_num)

    ############################################################################

    def remove_window(self, window):

        if window in self.windows:

            logging.debug("Removing window %s", window)
            window_idx = self.windows.index(window)

            if self.focused_window_num == window_idx:
                if self.focused_window_num > 0:
                    self.focused_window_num -= 1

            del self.windows[window_idx]
            self.draw_tabs()
            self.focus_window_num(self.focused_window_num)

    ############################################################################

    def resize_window(self, window):
        window.configure(width=self.width, height=self.height - self.client_y_offset)

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

        if len(self.windows) < 2:
            return

        next_win_num = self.focused_window_num + 1
        if next_win_num >= len(self.windows):
            next_win_num = 0

        self.focus_window_num(next_win_num)

    ############################################################################

    def cmd_prev_window(self):

        if len(self.windows) < 2:
            return

        prev_win_num = self.focused_window_num - 1
        if prev_win_num < 0:
            prev_win_num = len(self.windows) - 1

        self.focus_window_num(prev_win_num)

    ############################################################################

    def cmd_kill_window(self):

        if len(self.windows) == 0:
            return

        window = self.windows[self.focused_window_num]
        if self.wm_data.atoms.WM_DELETE_WINDOW in window.get_wm_protocols():
            delete_event = Xprotocol.event.ClientMessage(
                window=window,
                client_type=self.wm_data.atoms.WM_PROTOCOLS,
                data=(32, [self.wm_data.atoms.WM_DELETE_WINDOW, X.CurrentTime, 0, 0, 0]))
            window.send_event(delete_event)
        else:
            window.destroy()
