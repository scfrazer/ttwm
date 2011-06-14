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

    def add_window(self, window):

        logging.debug("Stack %d adding window %s", self.focused_stack_num, window)
        self.stacks[self.focused_stack_num].add_window(window)

    ############################################################################

    def remove_window(self, window):

        for stack in self.stacks:
            stack.remove_window(window)

    ############################################################################

    def do_cmd(self, cmd):

        if cmd in ['next_window', 'prev_window']:
            self.stacks[self.focused_stack_num].do_cmd(cmd)

    ############################################################################

    def handle_event(self, event):

        if event.type in [X.MapRequest, X.ConfigureRequest]:
            self.stacks[self.focused_stack_num].handle_event(event)
