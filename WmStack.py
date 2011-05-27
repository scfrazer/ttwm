# WmStack.py

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

        if claim_all_windows:
            self.claim_all_windows()

        if not self.windows:
            self.draw_empty_stack()

    ############################################################################

    def claim_all_windows(self):
        # TODO
        print self.width
        print self.height

    ############################################################################

    def draw_empty_stack(self):
        # TODO
        pass
