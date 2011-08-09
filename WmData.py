# WmData.py

import Xlib.X as X
import Xlib.XK as XK

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

    def parse_keys(self, display, config):

        section = 'Keys'

        if section not in config.sections():
            return

        commands = ['next_window',
                    'prev_window',
                    'kill_window']

        # TODO Handle multiple modifiers

        for key_def in config.options(section):

            (modifier, key) = key_def.split('+')

            if modifier == 'mod4':
                mod_mask = X.Mod4Mask
            elif modifier == 'mod3':
                mod_mask = X.Mod3Mask
            elif modifier == 'mod2':
                mod_mask = X.Mod2Mask
            elif modifier == 'mod1':
                mod_mask = X.Mod1Mask
            else:
                print "%s?" % (modifier)
                sys.exit(1)

            cmd = config.get(section, key_def)
            if cmd not in commands:
                print "Unknown command '%s' in '%s' section" % (cmd, section)
                sys.exit(1)

            keycode = display.keysym_to_keycode(XK.string_to_keysym(key))
            self.keys[(mod_mask, keycode)] = cmd
        colormap = self.display.screen(0).default_colormap

        self.ff_fg = colormap.alloc_named_color(self.ff_fg).pixel
        self.ff_bg = colormap.alloc_named_color(self.ff_bg).pixel
        self.ff_bo = colormap.alloc_named_color(self.ff_bo).pixel

        self.fu_fg = colormap.alloc_named_color(self.fu_fg).pixel
        self.fu_bg = colormap.alloc_named_color(self.fu_bg).pixel
        self.fu_bo = colormap.alloc_named_color(self.fu_bo).pixel

        self.uf_fg = colormap.alloc_named_color(self.uf_fg).pixel
        self.uf_bg = colormap.alloc_named_color(self.uf_bg).pixel
        self.uf_bo = colormap.alloc_named_color(self.uf_bo).pixel

        self.uu_fg = colormap.alloc_named_color(self.uu_fg).pixel
        self.uu_bg = colormap.alloc_named_color(self.uu_bg).pixel
        self.uu_bo = colormap.alloc_named_color(self.uu_bo).pixel

        self.bg = colormap.alloc_named_color(self.bg).pixel
        self.bo = colormap.alloc_named_color(self.bo).pixel

        self.active_fg = colormap.alloc_named_color(self.active_fg).pixel
        self.active_bg = colormap.alloc_named_color(self.active_bg).pixel
        self.active_bo = colormap.alloc_named_color(self.active_bo).pixel

        self.inactive_fg = colormap.alloc_named_color(self.inactive_fg).pixel
        self.inactive_bg = colormap.alloc_named_color(self.inactive_bg).pixel
        self.inactive_bo = colormap.alloc_named_color(self.inactive_bo).pixel

        self.fg = colormap.alloc_named_color(self.fg).pixel
        self.bg = colormap.alloc_named_color(self.bg).pixel
        self.bo = colormap.alloc_named_color(self.bo).pixel

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
