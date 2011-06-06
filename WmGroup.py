# WmGroup.py

from WmStack import WmStack

class WmGroup(object):

    def __init__(self, wm_data):

        self.wm_data = wm_data

        geom = wm_data.root.get_geometry()
        self.stacks = [WmStack(wm_data, top=0, left=0, width=geom.width, height=geom.height)]

    ############################################################################

    def add_windows(self, windows):
        self.stacks[0].add_windows(windows)
