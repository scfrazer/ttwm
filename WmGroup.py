# WmGroup.py

from WmStack import WmStack

class WmGroup(object):

    def __init__(self, display, root, config, pixel_colors, gcs, claim_all_windows=False):

        geom = root.get_geometry()
        self.stacks = [WmStack(display, root, config, pixel_colors, gcs,
                               top=0, left=0, width=geom.width, height=geom.height,
                               claim_all_windows=claim_all_windows)]
