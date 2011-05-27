# WmGroup.py

from WmStack import WmStack

class WmGroup(object):

    def __init__(self, display, root, config, claim_all_windows=False):

        self.display = display
        self.root = root
        self.config = config

        geom = self.root.get_geometry()
        self.stacks = [WmStack(display, root, config,
                               top=0, left=0, width=geom.width, height=geom.height,
                               claim_all_windows=claim_all_windows)]
