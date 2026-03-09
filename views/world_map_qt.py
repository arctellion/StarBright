from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QScrollArea, QWidget)
from PyQt6.QtCore import Qt, QPointF, QRectF, pyqtSignal, QByteArray
from PyQt6.QtGui import QPainter, QPen, QColor, QPolygonF, QFont, QBrush, QImage
from views.qt_components import Styles, GlassFrame
from travtools.world_map_gen import (SubMap, ICON_MOUNTAIN, ICON_OCEAN, ICON_CITY, ICON_STARPORT, 
    ICON_RUINS, ICON_CRATER, ICON_CROPLAND, ICON_TOWN, ICON_ARCOLOGY, ICON_PENAL)
import math

TERRAIN_PALETTE = {
    'Ocean': QColor("#1e3a8a"), 'Clear': QColor("#166534"), 'Mountain': QColor("#78350f"),
    'IceCap': QColor("#f1f5f9"), 'Ice Field': QColor("#bfdbfe"), 'Rough': QColor("#3f6212"),
    'Desert': QColor("#d97706"), 'Shore': QColor("#fcd34d"), 'Cropland': QColor("#84cc16"),
    'City': QColor("#6b7280"), 'Starport': QColor("#ffffff"), 'Islands': QColor("#a3e635"),
    'Resource': QColor("#facc15"), 'Twilight': QColor("#4a044e"), 'Ocean Depth': QColor("#0f172a"),
    'Crater': QColor("#57534e"), 'Woods': QColor("#14532d"), 'Abyss': QColor("#020617"),
    'Rural': QColor("#4ade80"), 'Grid': QColor("rgba(255, 255, 255, 20)"),
    'Ruins': QColor("#94a3b8"), 'Town': QColor("#cbd5e1"), 'Arcology': QColor("#e2e8f0"),
    'Penal': QColor("#ef4444"), 'Wasteland': QColor("#422006"), 'Exotic': QColor("#d946ef"),
    'Noble Lands': QColor("#8b5cf6"), 'Chasm': QColor("#0c0a09"), 'Precipice': QColor("#44403c"),
    'Frozen Lands': QColor("#93c5fd"), 'Sea': QColor("#2563eb")
}

class WorldMapWidget(QWidget):
    hex_clicked = pyqtSignal(object) 

    def __init__(self, map_data, size, is_submap=False):
        super().__init__()
        self.map_data = map_data
        self.world_size = size
        self.is_submap = is_submap
        
        # --- GEOMETRY FOR POINTY TOP HEXES ---
        self.hex_size = 20 # Radius
        self.hex_w = self.hex_size * math.sqrt(3)  # Width (flat side to flat side)
        self.hex_h = self.hex_size * 2             # Height (point to point)
        
        self.dx = self.hex_w                       # Horizontal step
        self.dy = self.hex_h * 0.75                # Vertical step

        self.scale = 1.0
        if not is_submap:
            if size > 15: self.scale = 0.4
            elif size > 10: self.scale = 0.6
            elif size > 6: self.scale = 0.8
        else:
            self.scale = 1.5 

        self.hex_hitboxes = [] 
        self.icons = {
            'Mountain': self.load_icon(ICON_MOUNTAIN),
            'Ocean': self.load_icon(ICON_OCEAN),
            'City': self.load_icon(ICON_CITY),
            'Starport': self.load_icon(ICON_STARPORT),
            'Ruins': self.load_icon(ICON_RUINS),
            'Crater': self.load_icon(ICON_CRATER),
            'Cropland': self.load_icon(ICON_CROPLAND),
            'Town': self.load_icon(ICON_TOWN),
            'Arcology': self.load_icon(ICON_ARCOLOGY),
            'Penal': self.load_icon(ICON_PENAL)
        }

        if not is_submap:
            mw = 6 * size * self.dx + 200
            mh = 5 * size * self.dy + 300
        else:
            mw, mh = 800, 600
            
        self.setMinimumSize(int(mw * self.scale), int(mh * self.scale))

    def load_icon(self, b64_string):
        data = QByteArray.fromBase64(b64_string.encode('utf-8'))
        img = QImage()
        if img.loadFromData(data, "SVG"):
            return img
        return None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#0a0a0a"))
        
        painter.scale(self.scale, self.scale)
        self.hex_hitboxes = []
        
        if not self.is_submap:
            self.draw_world_map(painter, TERRAIN_PALETTE)
        else:
            self.draw_sub_map(painter, TERRAIN_PALETTE)

    def draw_world_map(self, painter, palette):
        map_left = 100
        map_top = 100

        # Math for interlocking: Distance between centers of meshing triangles
        interlock_dx = (self.world_size * self.dx + self.dx) / 2
        tri_height = self.world_size * self.dy

        for tri in self.map_data:
            tid = tri['id']
            orientation = tri['orientation']
            
            if tid < 5: # North Row
                row, col = 0, tid
                # Shift by 0.5 hex to snap into the equator's staggered hex grid
                base_x = map_left + (col * 2) * interlock_dx + (0.5 * self.dx)
                base_y = map_top
            elif tid < 15: # Equator Row
                row, col = 1, tid - 5
                base_x = map_left + col * interlock_dx
                base_y = map_top + tri_height
            else: # South Row
                row, col = 2, tid - 15
                # Align with Equator Up triangles (odd cols: 1, 3, 5, 7, 9)
                base_x = map_left + (col * 2 + 1) * interlock_dx + (0.5 * self.dx)
                base_y = map_top + 2 * tri_height

            tri_width = self.world_size * self.dx
            cx = base_x + tri_width / 2
            
            for h in tri['hexes']:
                lx, ly = h['x'], h['y']
                
                if orientation == 1: # Point Up
                    row_width = ly + 1
                    px = cx + (lx - (row_width - 1) / 2.0) * self.dx
                    py = base_y + ly * self.dy
                else: # Point Down
                    row_width = self.world_size - ly
                    px = cx + (lx - (row_width - 1) / 2.0) * self.dx
                    py = base_y + ly * self.dy

                color = self.get_terrain_color(h['terrain'], palette)
                poly = self.draw_hex_pointy(painter, QPointF(px, py), color)
                self.draw_terrain_icon(painter, QPointF(px, py), h['terrain'])
                self.hex_hitboxes.append((poly, (tid, h['x'], h['y'])))

    def draw_sub_map(self, painter, palette):
        center_x, center_y = 400, 300
        for p, h in self.map_data.items():
            q, r = p
            px = center_x + self.dx * (q + r/2.0)
            py = center_y + self.dy * r
            
            color = self.get_terrain_color(h.terrain, palette)
            poly = self.draw_hex_pointy(painter, QPointF(px, py), color)
            self.draw_terrain_icon(painter, QPointF(px, py), h.terrain)
            self.hex_hitboxes.append((poly, (None, q, r)))

    def get_terrain_color(self, terrain, palette):
        if 'Starport' in terrain: return palette['Starport']
        if 'Arcology' in terrain: return palette['Arcology']
        if 'City' in terrain: return palette['City']
        if 'Town' in terrain: return palette['Town']
        if 'Noble Lands' in terrain: return palette['Noble Lands']
        if 'Exotic' in terrain: return palette['Exotic']
        if 'Penal' in terrain: return palette['Penal']
        if 'IceCap' in terrain: return palette['IceCap']
        if 'Ice Field' in terrain: return palette['Ice Field']
        if 'Frozen Lands' in terrain: return palette['Frozen Lands']
        if 'Ocean Depth' in terrain: return palette['Ocean Depth']
        if 'Ocean' in terrain: return palette['Ocean']
        if 'Sea' in terrain: return palette['Sea']
        if 'Mountain' in terrain: return palette['Mountain']
        if 'Chasm' in terrain: return palette['Chasm']
        if 'Precipice' in terrain: return palette['Precipice']
        if 'Shore' in terrain: return palette['Shore']
        if 'Islands' in terrain: return palette['Islands']
        if 'Cropland' in terrain: return palette['Cropland']
        if 'Desert' in terrain: return palette['Desert']
        if 'Wasteland' in terrain: return palette['Wasteland']
        if 'Ruins' in terrain: return palette['Ruins']
        if 'Crater' in terrain: return palette['Crater']
        if 'Resource' in terrain: return palette['Resource']
        if 'Rural' in terrain: return palette['Rural']
        return palette['Clear']

    def draw_terrain_icon(self, painter, center, terrain):
        icon = None
        if 'Starport' in terrain: icon = self.icons['Starport']
        elif 'Arcology' in terrain: icon = self.icons['Arcology']
        elif 'City' in terrain: icon = self.icons['City']
        elif 'Town' in terrain: icon = self.icons['Town']
        elif 'Mountain' in terrain: icon = self.icons['Mountain']
        elif 'Ruins' in terrain: icon = self.icons['Ruins']
        elif 'Crater' in terrain: icon = self.icons['Crater']
        elif 'Cropland' in terrain: icon = self.icons['Cropland']
        elif 'Penal' in terrain: icon = self.icons['Penal']
        
        if icon:
            rect = QRectF(center.x() - 10, center.y() - 10, 20, 20)
            painter.drawImage(rect, icon)

    def get_visible_terrains(self):
        visible = set()
        if not self.is_submap:
            for tri in self.map_data:
                for h in tri['hexes']:
                    for t in h['terrain']: visible.add(t)
        else:
            for h in self.map_data.values():
                for t in h.terrain: visible.add(t)
        return list(visible)

    def draw_hex_pointy(self, painter, center, color):
        x, y = center.x(), center.y()
        s = self.hex_size
        points = []
        for i in range(6):
            angle_deg = 60 * i - 90
            angle_rad = math.pi / 180 * angle_deg
            px = x + s * math.cos(angle_rad)
            py = y + s * math.sin(angle_rad)
            points.append(QPointF(px, py))
            
        poly = QPolygonF(points)
        painter.setBrush(color)
        painter.setPen(QPen(QColor(255, 255, 255, 20), 0.5))
        painter.drawPolygon(poly)
        return poly

    def mousePressEvent(self, event):
        pos = event.position() / self.scale
        for poly, data in self.hex_hitboxes:
            if poly.containsPoint(pos, Qt.FillRule.WindingFill):
                self.hex_clicked.emit(data)
                break

# ... (WorldMapDialog class remains the same)

class WorldMapDialog(QDialog):
    """The Main Window for the Map Viewer."""
    def __init__(self, generator, world_name, parent=None):
        super().__init__(parent)
        self.generator = generator
        self.world_name = world_name
        self.uwp = generator.uwp
        self.history = [] # Stack of (view_data, is_submap, title)
        
        self.setWindowTitle(f"Stellar Cartography: {world_name}")
        self.resize(1200, 900)
        self.init_ui()
        
        # Start with World View
        self.show_map(self.generator.get_map_json(), False, "Planetary Overview (World Level)")

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.setStyleSheet(f"background-color: {Styles.BG_COLOR}; color: white;")
        
        # Header
        self.header = QFrame()
        self.header.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1a1a1a, stop:1 #000); border-bottom: 2px solid #333; padding: 10px;")
        h_layout = QVBoxLayout(self.header)
        
        self.title_lbl = QLabel(f"<span style='font-size: 24px; font-weight: bold; color: {Styles.AMBER};'>{self.world_name}</span>")
        self.uwp_lbl = QLabel(f"<span style='font-size: 16px; color: #aaa;'>UWP: {self.uwp} | </span><span id='level_lbl' style='color: #60a5fa;'>Loading...</span>")
        h_layout.addWidget(self.title_lbl)
        h_layout.addWidget(self.uwp_lbl)
        self.main_layout.addWidget(self.header)

        # Mapping Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background-color: #000; border: none;")
        self.main_layout.addWidget(self.scroll)

        # Dynamic Legend Area
        self.legend_frame = QFrame()
        self.legend_frame.setStyleSheet("background: #111; border-top: 1px solid #333; padding: 5px;")
        self.legend_layout = QHBoxLayout(self.legend_frame)
        self.main_layout.addWidget(self.legend_frame)

        # Bottom Bar
        self.footer = QHBoxLayout()
        self.btn_back = QPushButton("▲ Back to Higher Level")
        self.btn_back.clicked.connect(self.go_back)
        self.btn_back.setEnabled(False)
        self.btn_back.setFixedSize(200, 40)
        self.btn_back.setStyleSheet(f"background-color: {Styles.BORDER_COLOR}; border-radius: 5px;")
        
        self.footer.addWidget(self.btn_back)
        self.footer.addStretch()
        
        btn_close = QPushButton("Close Control")
        btn_close.clicked.connect(self.close)
        btn_close.setFixedSize(150, 40)
        btn_close.setStyleSheet(f"background-color: #7f1d1d; border-radius: 5px;")
        self.footer.addWidget(btn_close)
        self.main_layout.addLayout(self.footer)

    def show_map(self, data, is_submap, title):
        self.history.append((data, is_submap, title))
        self.render_current()

    def render_current(self):
        data, is_submap, title = self.history[-1]
        self.uwp_lbl.setText(f"<span style='font-size: 16px; color: #aaa;'>UWP: {self.uwp} | </span><span style='color: #60a5fa;'>{title}</span>")
        
        self.map_widget = WorldMapWidget(data, self.generator.size, is_submap)
        self.map_widget.hex_clicked.connect(self.handle_hex_click)
        self.scroll.setWidget(self.map_widget)
        
        # Update Legend
        self.update_legend()
        
        self.btn_back.setEnabled(len(self.history) > 1)
        if len(self.history) > 1:
            self.btn_back.setStyleSheet(f"background-color: {Styles.BLUE}; font-weight: bold; border-radius: 5px;")
        else:
            self.btn_back.setStyleSheet(f"background-color: {Styles.BORDER_COLOR}; border-radius: 5px;")

    def update_legend(self):
        # Clear existing legend
        for i in reversed(range(self.legend_layout.count())): 
            widget = self.legend_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        visible_terrains = self.map_widget.get_visible_terrains()
        if not visible_terrains:
            self.legend_frame.hide()
            return
            
        self.legend_frame.show()
        self.legend_layout.addWidget(QLabel("<b>Map Legend:</b>"))
        
        for t in visible_terrains:
            color = TERRAIN_PALETTE.get(t, QColor("#fff"))
            dot = QLabel("  ")
            dot.setFixedSize(16, 16)
            dot.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #555; border-radius: 3px;")
            label = QLabel(t)
            label.setStyleSheet("color: #ccc; margin-right: 15px;")
            self.legend_layout.addWidget(dot)
            self.legend_layout.addWidget(label)
        
        self.legend_layout.addStretch()

    def handle_hex_click(self, data):
        if len(self.history) >= 4: return # World -> Terrain -> Local -> Single
        
        # Import SubMap here to avoid circular dependency issues if needed, 
        # though it is imported at top now.
        # from travtools.world_map_gen import SubMap 
        
        if data[0] is not None: # World level click (tid, x, y)
            submap = self.generator.subdivide_hex(*data)
            if submap:
                level_name = "Terrain Level (100km Hexes)" if len(self.history) == 1 else "Local Level (10km Hexes)"
                self.show_map(submap.hexes, True, level_name)
        else: # Submap level click (None, q, r)
            # Find the hex object in the current submap data
            current_hexes = self.history[-1][0]
            target_hex = current_hexes.get((data[1], data[2]))
            if target_hex:
                if not target_hex.sub_map:
                    target_hex.sub_map = SubMap(target_hex, "Local", self.generator.rng)
                level_name = "Local Level (10km Hexes)" if len(self.history) == 2 else "Single Hex Level (1km Hexes)"
                self.show_map(target_hex.sub_map.hexes, True, level_name)

    def go_back(self):
        if len(self.history) > 1:
            self.history.pop()
            self.render_current()