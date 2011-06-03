# WmStack.py

import Xlib.X as X

class WmStack(object):

    def __init__(self, display, root, config, pixel_colors, gcs,
                 top, left, width, height,
                 claim_all_windows):

        self.display = display
        self.root = root
        self.config = config
        self.pixel_colors = pixel_colors
        self.gcs = gcs

        border_width = self.config.display['border_width']
        self.top = top
        self.left = left
        self.width = width - 2 * border_width
        self.height = height - 2 * border_width

        self.windows = []

        self.create_parent_window()

        if claim_all_windows:
            self.claim_all_windows()

        self.parent_window.map()

        self.tabs = []
        self.update_tabs()

    ############################################################################

    def create_parent_window(self):

        self.parent_window = self.root.create_window(self.top, self.left, self.width, self.height,
                                                     self.config.display['border_width'],
                                                     X.CopyFromParent, X.InputOutput, X.CopyFromParent,
                                                     border_pixel=self.pixel_colors['active_selected_bg'])

    ############################################################################

    def claim_all_windows(self):

        windows = self.root.query_tree().children
        for window in windows:
            if not window.get_wm_name():
                continue
            attrs = window.get_attributes()
            if attrs.override_redirect or attrs.map_state == X.IsUnmapped:
                continue
            self.windows.append(window)
            window.change_save_set(X.SetModeInsert)
            window.reparent(self.parent_window, 0, self.config.display['tab_height'])

    ############################################################################

    def update_tabs(self):

        # TODO Destroy existing tabs

        if self.tabs:
            pass

        tab_width = self.width / len(self.windows)
        tab_width_leftover = self.width % len(self.windows)

        # TODO Limit number of tabs

        self.tabs = []
        left_edge = 0
        for (idx, window) in enumerate(self.windows):

            width = tab_width
            if idx < tab_width_leftover:
                width += 1

            tab = self.parent_window.create_window(left_edge, 0, width, self.config.display['tab_height'],
                                                   0, X.CopyFromParent, X.InputOutput, X.CopyFromParent,
                                                   background_pixel=self.pixel_colors['active_selected_bg'])
            left_edge += width

            tab.map()

            title_text = window.get_wm_name()
            title_text_extents = self.gcs['active_selected'].query_text_extents(title_text)
            tab.draw_text(self.gcs['active_selected'],
                          (width - title_text_extents.overall_width) / 2, 13,  # TODO
                          title_text)

            self.tabs.append(tab)
