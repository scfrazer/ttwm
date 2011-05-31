# WmStack.py

import Xlib.X

class WmStack(object):

    def __init__(self, display, root, config,
                 top, left, width, height,
                 claim_all_windows):

        self.display = display
        self.root = root
        self.config = config
        self.top = top
        self.left = left
        self.width = width
        self.height = height

        self.windows = []

        self.create_parent_window()

        if claim_all_windows:
            self.claim_all_windows()

    ############################################################################

    def create_parent_window(self):

        self.parent_window = self.root.create_window(self.top, self.left, self.width, self.height,
                                                     self.config.display_opts['border_width'],
                                                     Xlib.X.CopyFromParent)
        self.parent_window.map()

    ############################################################################

    def claim_all_windows(self):

        windows = self.root.query_tree().children
        for window in windows:
            if not window.get_wm_name():
                continue
            attrs = window.get_attributes()
            if attrs.override_redirect or attrs.map_state == Xlib.X.IsUnmapped:
                continue
            self.windows.append(window)
            window.reparent(self.parent_window, 10, 10)  # TODO
