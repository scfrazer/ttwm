# WmGroup.py

import logging
from WmStack import WmStack

class WmGroup(object):

    def __init__(self, name, wm_data):

        self.name = name
        self.wm_data = wm_data

        self.event_dispatch = {}

        self.cmd_dispatch = {
            'split_horizontal': self.cmd_split_horizontal,
            'split_vertical': self.cmd_split_vertical,
            'next_stack': self.cmd_next_stack,
            'prev_stack': self.cmd_prev_stack,
            'kill_stack': self.cmd_kill_stack
            }

        geom = wm_data.root.get_geometry()
        self.stacks = [WmStack(wm_data, top=0, left=0,
                               width=geom.width, height=geom.height - wm_data.status_bar.height)]
        self.focused_stack_num = 0

    ############################################################################

    def add_window(self, window):

        logging.debug("Group %s, stack %d adding window %s",
                      self.name, self.focused_stack_num, window)
        self.stacks[self.focused_stack_num].add_window(window)

    ############################################################################

    def remove_window(self, window):

        for stack in self.stacks:
            stack.remove_window(window)

    ############################################################################

    def num_windows(self):

        num_windows = 0
        for stack in self.stacks:
            num_windows += len(stack.windows)

        return num_windows

    ############################################################################

    def do_cmd(self, cmd):

        if cmd in self.cmd_dispatch:
            logging.debug(cmd)
            self.cmd_dispatch[cmd]()
        else:
            self.stacks[self.focused_stack_num].do_cmd(cmd)

    ############################################################################

    def handle_event(self, event):

        if event.type in self.event_dispatch:
            self.event_dispatch[event.type](event)
        else:
            self.stacks[self.focused_stack_num].handle_event(event)

    ############################################################################

    def cmd_split_horizontal(self):
        pass

    ############################################################################

    def cmd_split_vertical(self):
        pass

    ############################################################################

    def cmd_next_stack(self):
        pass

    ############################################################################

    def cmd_prev_stack(self):
        pass

    ############################################################################

    def cmd_kill_stack(self):
        pass
