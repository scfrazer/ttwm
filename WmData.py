# WmData.py

class WmDataGC(object):
    pass

################################################################################

class WmDataAtoms(object):
    pass

################################################################################

class WmData(object):

    def __init__(self, display, screen, config):

        self.display = display
        self.screen = screen
        self.root = screen.root
        self.config = config

        self.config.colors.pixelize_colors(screen)
        self.setup_metrics_and_gcs()
        self.setup_atoms()

    ############################################################################

    def setup_metrics_and_gcs(self):

        self.gcs = WmDataGC()

        # Tabs

        title_font = self.display.open_font(self.config.fonts.title)
        query = title_font.query()
        self.config.fonts.title_height = query.font_ascent + query.font_descent
        # TODO 4 = 1 pad + 1 border on top/bottom ... should be configurable
        self.config.display.tab_height = self.config.fonts.title_height + 4

        self.gcs.tab_ff = self.root.create_gc(font=title_font,
                                              foreground=self.config.colors.tab_ff_fg,
                                              background=self.config.colors.tab_ff_bg)

        self.gcs.tab_fu = self.root.create_gc(font=title_font,
                                              foreground=self.config.colors.tab_fu_fg,
                                              background=self.config.colors.tab_fu_bg)

        self.gcs.tab_uf = self.root.create_gc(font=title_font,
                                              foreground=self.config.colors.tab_uf_fg,
                                              background=self.config.colors.tab_uf_bg)

        self.gcs.tab_uu = self.root.create_gc(font=title_font,
                                              foreground=self.config.colors.tab_uu_fg,
                                              background=self.config.colors.tab_uu_bg)

        # Status bar

        group_font = self.display.open_font(self.config.fonts.group)
        query = title_font.query()
        self.config.fonts.group_height = query.font_ascent + query.font_descent
        # TODO 4 = 1 pad + 1 border on top/bottom ... should be configurable
        self.config.display.status_height = self.config.fonts.group_height + 4

        # TODO Change 'group' to 'status', add gcs for groups and status

    ############################################################################

    def setup_atoms(self):

        self.atoms = WmDataAtoms()
        self.atoms.WM_PROTOCOLS = self.display.intern_atom('WM_PROTOCOLS')
        self.atoms.WM_DELETE_WINDOW = self.display.intern_atom('WM_DELETE_WINDOW')
