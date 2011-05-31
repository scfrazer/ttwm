# WmStack.py

import Xlib.X as X

class WmStack(object):

    def __init__(self, display, root, config,
                 top, left, width, height,
                 claim_all_windows):

        self.display = display
        self.root = root
        self.config = config

        border_width = self.config.display_opts['border_width']
        self.top = top
        self.left = left
        self.width = width - 2 * border_width
        self.height = height - 2 * border_width

        self.windows = []

        self.create_parent_window()

        if claim_all_windows:
            self.claim_all_windows()

    ############################################################################

    def create_parent_window(self):

        # colormap = self.root.get_attributes().colormap
        # border = colormap.alloc_color(0xff, 0x00, 0x00)
        self.parent_window = self.root.create_window(self.top, self.left, self.width, self.height,
                                                     self.config.display_opts['border_width'],
                                                     X.CopyFromParent, X.InputOutput, X.CopyFromParent,
                                                     border_pixel=0xFF0000)
        self.parent_window.map()

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
            window.reparent(self.parent_window, 10, 10)  # TODO
