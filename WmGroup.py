# WmGroup.py

from WmStack import WmStack

class WmGroup(object):

    def __init__(self, display, root, config):

        self.display = display
        self.root = root
        self.config = config

        self.init_stacks()

    ############################################################################

    def claim_all_windows(self):
        pass

    ############################################################################

    def init_stacks(self):
        self.stacks = []
