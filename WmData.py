# WmData.py

class WmData(object):

    def __init__(self, display, screen, config):

        self.display = display
        self.screen = screen
        self.root = screen.root
        self.config = config

        self.setup_colors()
        self.setup_gcs()

    ############################################################################

    def setup_colors(self):

        self.pixel_colors = {}

        colormap = self.screen.default_colormap

        for (color_name, color_value) in self.config.colors.iteritems():
            color = colormap.alloc_named_color(color_value)
            self.pixel_colors[color_name] = color.pixel

    ############################################################################

    def setup_gcs(self):

        self.gcs = {}

        font = self.display.open_font(self.config.fonts['title'])

        query = font.query()
        # TODO 4 = 1 pad + 1 border on top/bottom ... should be configurable
        self.config.fonts['title_height'] = query.font_ascent + query.font_descent
        self.config.display['tab_height'] = self.config.fonts['title_height'] + 4

        for name in ['active_selected', 'active_unselected',
                     'inactive_selected', 'inactive_unselected']:

            self.gcs[name] = self.root.create_gc(font=font,
                                                 foreground=self.pixel_colors[name + '_fg'],
                                                 background=self.pixel_colors[name + '_bg'])
