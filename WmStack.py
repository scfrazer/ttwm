# WmStack.py

import Xlib.X as X

class WmStack(object):

    def __init__(self, wm_data, top, left, width, height):

        self.wm_data = wm_data

        border_width = self.wm_data.config.display['border_width']
        self.top = top
        self.left = left
        self.width = width - 2 * border_width
        self.height = height - 2 * border_width

        self.left_windows = []
        self.tab_windows = []
        self.right_windows = []

        self.active_window_num = 0  # This is an index into self.tabbed_windows

        self.create_parent_window()
        self.parent_window.map()

        self.tabs = []
        self.update_tabs()

    ############################################################################

    def create_parent_window(self):

        self.parent_window = self.wm_data.root.create_window(
            self.top, self.left, self.width, self.height,
            self.wm_data.config.display['border_width'],
            X.CopyFromParent, X.InputOutput, X.CopyFromParent,
            border_pixel=self.wm_data.pixel_colors['active_selected_bg'])

    ############################################################################

    def update_tabs(self):

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
        for (idx, window) in enumerate(self.tab_windows):

            width = tab_width
            if idx < tab_width_leftover:
                width += 1

            if idx == self.active_window_num:
                gc = self.wm_data.gcs['active_selected']
                background_pixel = self.wm_data.pixel_colors['active_selected_bg']
            else:
                gc = self.wm_data.gcs['active_unselected']
                background_pixel = self.wm_data.pixel_colors['active_unselected_bg']

            tab = self.parent_window.create_window(
                left_edge, 0, width, self.wm_data.config.display['tab_height'],
                0, X.CopyFromParent, X.InputOutput, X.CopyFromParent,
                background_pixel=background_pixel)

            left_edge += width

            tab.map()

            title_text = window.get_wm_name()
            title_text_extents = gc.query_text_extents(title_text)
            tab.draw_text(gc, (width - title_text_extents.overall_width) / 2,
                          self.wm_data.config.fonts['title_height'], title_text)

            self.tabs.append(tab)

    ############################################################################

    def add_windows(self, windows):

        # TODO Limit number of tabs

        for window in windows:
            window.reparent(self.parent_window, 0, self.wm_data.config.display['tab_height'])
            self.tab_windows.insert(0, window)

        self.update_tabs()
