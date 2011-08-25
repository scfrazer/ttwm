# WmStack.py

import logging
import Xlib.X as X
import Xlib.protocol as Xprotocol

class WmStack(object):

    def __init__(self, wm_data, x, y, width, height):

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

        logging.debug('New stack x=%d y=%d width=%d height=%d', x, y, width, height)

        self.x = x
        self.y = y
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
            self.x, self.y, self.width, self.height,
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
        self.tabs = []

        if len(self.windows) == 0:
            self.parent_window.clear_area(0, 0, self.width, self.height)
            self.focused_window_num = 0
            self.create_tab(0, self.width)
            self.update_tab(0)
            return

        tab_width = self.width / len(self.windows)
        tab_width_leftover = self.width % len(self.windows)

        x = 0
        for (tab_num, window) in enumerate(self.windows):

            width = tab_width
            if tab_num < tab_width_leftover:
                width += 1

            tab = self.create_tab(x, width)
            self.update_tab(tab_num)

            x += width

    ############################################################################

    def create_tab(self, x, width):

        tab = self.parent_window.create_window(
            x, 0 - self.wm_data.stack.border_width,
            width - 2 * self.wm_data.tab.border_width,
            self.wm_data.tab.height - 2 * self.wm_data.tab.border_width,
            self.wm_data.tab.border_width,
            X.CopyFromParent, X.InputOutput, X.CopyFromParent)

        tab.map()
        self.tabs.append(tab)

        return tab

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

        if len(self.windows) == 0:
            title_text = "<Empty>"
        else:
            title_text = self.windows[tab_num].get_wm_name()
        title_text_extents = gc.query_text_extents(title_text)

        geom = tab.get_geometry()

        tab.clear_area(width=geom.width, height=geom.height)
        tab.draw_text(gc, (geom.width - title_text_extents.overall_width) / 2,
                      self.wm_data.tab.font_y_offset, title_text)

    ############################################################################

    def unfocus(self):

        self.focused = False
        for tab_num in xrange(len(self.tabs)):
            self.update_tab(tab_num)

    ############################################################################

    def focus(self):

        self.focused = True
        for tab_num in xrange(len(self.tabs)):
            self.update_tab(tab_num)
        if len(self.windows) > 0:
            self.focus_window_num(self.focused_window_num)
        else:
            self.parent_window.set_input_focus(X.RevertToPointerRoot, X.CurrentTime)

    ############################################################################

    def resize(self, x, y, width, height):

        logging.debug('Resizing stack to x=%d y=%d width=%d height=%d', x, y, width, height)

        self.x = x
        self.y = y
        self.width = width - 2 * self.wm_data.stack.border_width
        self.height = height - 2 * self.wm_data.stack.border_width

        self.parent_window.configure(x=self.x, y=self.y, width=self.width, height=self.height)
        for window in self.windows:
            self.resize_client_window(window)
        self.draw_tabs()

    ############################################################################

    def add_window(self, window):

        logging.debug("Adding window '%s' %s", window.get_wm_name(), window)

        # Turn off SubstructureNotifyMask during reparent to avoid spurious UnmapNotify

        self.wm_data.root.change_attributes(event_mask=X.SubstructureRedirectMask)
        window.reparent(self.parent_window, 0, self.client_y_offset)
        self.wm_data.root.change_attributes(event_mask=(X.SubstructureRedirectMask
                                                        | X.SubstructureNotifyMask))
        self.resize_client_window(window)

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
        logging.debug("Focusing window '%s' %s" % (window.get_wm_name(), window))
        window.map()
        window.configure(stack_mode=X.Above)
        window.set_input_focus(X.RevertToPointerRoot, X.CurrentTime)

        if window_num != self.focused_window_num:
            old_focused_window_num = self.focused_window_num
            self.focused_window_num = window_num
            self.update_tab(old_focused_window_num)
            self.update_tab(self.focused_window_num)
            self.windows[old_focused_window_num].unmap()

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

    def resize_client_window(self, window):

        window.configure(width=self.width, height=self.height - self.client_y_offset)

    ############################################################################

    def handle_event(self, event):

        if event.type in self.event_dispatch:
            self.event_dispatch[event.type](event)

    ############################################################################

    def event_map_request(self, event):

        logging.debug("MapRequest for window '%s' %s", event.window.get_wm_name(), event.window)
        self.add_window(event.window)

    ############################################################################

    def event_configure_request(self, event):

        logging.debug("ConfigureRequest for window '%s' %s", event.window.get_wm_name(), event.window)
        self.resize_client_window(event.window)

    ############################################################################

    def do_cmd(self, cmd):

        if cmd in self.cmd_dispatch:
            if self.windows:
                window = self.windows[self.focused_window_num]
                logging.debug("%s, focused window is '%s' %s" % (cmd, window.get_wm_name(), window))
            else:
                logging.debug("%s, no focused window" % (cmd))
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
