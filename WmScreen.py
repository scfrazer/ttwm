# WmScreen.py

class WmScreen(object):

    def __init__(self, screen, config):

        self.root_window = screen.root
        self.width = screen.width_in_pixels
        self.height = screen.height_in_pixels

        self.config = config

        print screen.width_in_pixels
        print screen.height_in_pixels
