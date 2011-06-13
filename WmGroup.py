# WmGroup.py

import logging
import Xlib.X as X
from WmStack import WmStack

class WmGroup(object):

    def __init__(self, wm_data):

        self.wm_data = wm_data

        geom = wm_data.root.get_geometry()
        self.stacks = [WmStack(wm_data, top=0, left=0, width=geom.width, height=geom.height)]
        self.focused_stack_num = 0

    ############################################################################

    def add_windows(self, windows):
        logging.debug("Stack %d adding %d windows", self.focused_stack_num, len(windows))
        self.stacks[self.focused_stack_num].add_windows(windows)

    ############################################################################

    def do_cmd(self, cmd):

        if cmd in ['next_window', 'prev_window']:
            self.stacks[self.focused_stack_num].do_cmd(cmd)

    ############################################################################

    def handle_event(self, event):

        if event.type in [X.MapRequest, X.ConfigureRequest]:
            self.stacks[self.focused_stack_num].handle_event(event)
