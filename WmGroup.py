# WmGroup.py

import logging
from WmStack import WmStack

class WmGroup(object):

    def __init__(self, name, wm_data):

        self.name = name
        self.wm_data = wm_data
        self.tab = None

        self.event_dispatch = {}

        self.cmd_dispatch = {
            'split_horizontal': self.cmd_split_horizontal,
            'split_vertical': self.cmd_split_vertical,
            'next_stack': self.cmd_next_stack,
            'prev_stack': self.cmd_prev_stack,
            'kill_stack': self.cmd_kill_stack
            }

        geom = wm_data.root.get_geometry()
        self.stacks = [WmStack(wm_data, x=0, y=0,
                               width=geom.width, height=geom.height - wm_data.status_bar.height)]
        self.focused_stack_num = 0
        self.focus_stack_num(self.focused_stack_num)

    ############################################################################

    def add_window(self, window):

        logging.debug("Group %s, stack %d adding window %s",
                      self.name, self.focused_stack_num, window)
        self.stacks[self.focused_stack_num].add_window(window)

    ############################################################################

    def add_transient(self, top_window, window):

        logging.debug("Group %s, stack %d adding transient %s to window %s",
                      self.name, self.focused_stack_num, window, top_window)

        # TODO Add transient windows
        pass

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

    def focus_stack_num(self, stack_num):

        logging.debug("Focusing stack %d" % (stack_num))
        if self.focused_stack_num != stack_num:
            self.stacks[self.focused_stack_num].unfocus()
        self.focused_stack_num = stack_num
        self.stacks[self.focused_stack_num].focus()

    ############################################################################

    def cmd_split_horizontal(self):

        cur_stack = self.stacks[self.focused_stack_num]
        cur_stack_width = cur_stack.width + 2 * self.wm_data.stack.border_width
        cur_stack_height = cur_stack.height + 2 * self.wm_data.stack.border_width

        new_stack_width = cur_stack_width // 2
        cur_stack_width -= new_stack_width
        cur_stack.resize(cur_stack.x, cur_stack.y, cur_stack_width, cur_stack_height)

        self.stacks.insert(self.focused_stack_num + 1,
                           WmStack(self.wm_data,
                                   x=cur_stack.x + cur_stack_width,
                                   y=cur_stack.y,
                                   width=new_stack_width,
                                   height=cur_stack_height))

        self.focus_stack_num(self.focused_stack_num + 1)

    ############################################################################

    def cmd_split_vertical(self):

        cur_stack = self.stacks[self.focused_stack_num]
        cur_stack_width = cur_stack.width + 2 * self.wm_data.stack.border_width
        cur_stack_height = cur_stack.height + 2 * self.wm_data.stack.border_width

        new_stack_height = cur_stack_height // 2
        cur_stack_height -= new_stack_height
        cur_stack.resize(cur_stack.x, cur_stack.y, cur_stack_width, cur_stack_height)

        self.stacks.insert(self.focused_stack_num + 1,
                           WmStack(self.wm_data,
                                   x=cur_stack.x,
                                   y=cur_stack.y + cur_stack_height,
                                   width=cur_stack_width,
                                   height=new_stack_height))

        self.focus_stack_num(self.focused_stack_num + 1)

    ############################################################################

    def cmd_next_stack(self):

        if len(self.stacks) < 2:
            return

        next_stack_num = self.focused_stack_num + 1
        if next_stack_num >= len(self.stacks):
            next_stack_num = 0
        self.focus_stack_num(next_stack_num)

    ############################################################################

    def cmd_prev_stack(self):

        if len(self.stacks) < 2:
            return

        prev_stack_num = self.focused_stack_num - 1
        if prev_stack_num < 0:
            prev_stack_num = len(self.stacks) - 1
        self.focus_stack_num(prev_stack_num)

    ############################################################################

    def cmd_kill_stack(self):

        if len(self.stacks) < 2:
            return

        # TODO Implement kill stack
