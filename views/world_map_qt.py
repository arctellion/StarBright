from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QScrollArea, QWidget)
from PyQt6.QtCore import Qt, QPointF, QRectF, pyqtSignal, QByteArray
from PyQt6.QtGui import QPainter, QPen, QColor, QPolygonF, QFont, QBrush, QImage
from views.qt_components import Styles, GlassFrame
from travtools.world_map_gen import SubMap, ICON_MOUNTAIN, ICON_OCEAN, ICON_CITY, ICON_STARPORT
import math

TERRAIN_PALETTE = {
    'Ocean': QColor("#1e3a8a"), 'Clear': QColor("#166534"), 'Mountain': QColor("#78350f"),
    'IceCap': QColor("#f1f5f9"), 'Ice Field': QColor("#bfdbfe"), 'Rough': QColor("#3f6212"),
    'Desert': QColor("#d97706"), 'Shore': QColor("#fcd34d"), 'Cropland': QColor("#84cc16"),
    'City': QColor("#6b7280"), 'Starport': QColor("#ffffff"), 'Islands': QColor("#a3e635"),
    'Resource': QColor("#facc15"), 'Twilight': QColor("#4a044e"), 'Ocean Depth': QColor("#0f172a"),
    'Crater': QColor("#57534e"), 'Woods': QColor("#14532d"), 'Abyss': QColor("#020617"),
    'Rural': QColor("#4ade80"),
    'Grid': QColor("rgba(255, 255, 255, 20)")
}

class WorldMapWidget(QWidget):
    hex_clicked = pyqtSignal(object) 

    def __init__(self, map_data, size, is_submap=False, context_data=None):
        super().__init__()
        self.map_data = map_data
        self.world_size = size
        self.is_submap = is_submap
        self.context_data = context_data # Dictionary of submaps for neighbor rendering
        
        # --- GEOMETRY FOR POINTY TOP HEXES ---
        self.hex_size = 16 # Radius
        self.hex_w = self.hex_size * math.sqrt(3) # Width (flat-to-flat)
        self.hex_h = self.hex_size * 2            # Height (point-to-point)
        
        self.dx = self.hex_w            # Horizontal step
        self.dy = self.hex_h * 0.75     # Vertical step

        self.scale = 1.0
        if not is_submap:
            if size > 15: self.scale = 0.5
            elif size > 10: self.scale = 0.7
            elif size > 6: self.scale = 0.85
        else:
            self.scale = 2.5 # Zoomed in view for details

        self.hex_hitboxes = [] 
        self.icons = {
            'Mountain': self.load_icon(ICON_MOUNTAIN),
            'Ocean': self.load_icon(ICON_OCEAN),
            'City': self.load_icon(ICON_CITY),
            'Starport': self.load_icon(ICON_STARPORT)
        }

        # Widget Size
        if not is_submap:
            mw = 6 * size * self.dx + 200
            mh = 5 * size * self.dy + 300
        else:
            mw, mh = 800, 600 # Larger window for detail view
            
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
        map_left = 80
        map_top = 60

        for tri in self.map_data:
            tid = tri['id']
            row = tid // 5
            col = tid % 5
            orientation = tri['orientation']
            
            # --- Layout Calculation ---
            # Strip Layout:
            # Col Offset: Each triangle takes up (Size * dx) width.
            base_x = map_left + col * (self.world_size * self.dx)
            
            # Row Offset:
            # Row 0: Top.
            # Row 1: Starts at bottom of Row 0? No, Row 0 is Point Down. 
            # Row 0 Height = Size * dy.
            # Row 1 (Point Up) starts at Top of Row 0? No, they interlock.
            
            # Standard Traveller Map visual alignment:
            # The triangles are adjacent.
            # Point Down Triangle: Bounding Box Height = Size * dy.
            # Point Up Triangle: Bounding Box Height = Size * dy.
            
            base_y = map_top + row * (self.world_size * self.dy)

            # --- Draw Hexes ---
            for h in tri['hexes']:
                lx, ly = h['x'], h['y']
                px, py = 0, 0
                
                # Centering logic for the Triangle Shape
                if orientation == 0: # Point Down
                    row_width = ly + 1
                    # Calculate center of the row
                    center_x = base_x + (self.world_size * self.dx / 2)
                    # Shift left by half the row width
                    start_x = center_x - (row_width * self.dx / 2)
                    
                    px = start_x + (lx * self.dx) + (self.dx / 2)
                    py = base_y + (ly * self.dy) + (self.hex_size)
                    
                else: # Point Up
                    row_width = self.world_size - ly
                    center_x = base_x + (self.world_size * self.dx / 2)
                    start_x = center_x - (row_width * self.dx / 2)
                    
                    px = start_x + (lx * self.dx) + (self.dx / 2)
                    py = base_y + (ly * self.dy) + (self.hex_size)

                color = self.get_terrain_color(h['terrain'], palette)
                poly = self.draw_hex_pointy(painter, QPointF(px, py), color)
                self.draw_terrain_icon(painter, QPointF(px, py), h['terrain'])
                self.hex_hitboxes.append((poly, (tid, h['x'], h['y'])))

    def draw_sub_map(self, painter, palette):
        # Center of the viewport
        center_x, center_y = 400, 300
        
        # Draw Context (Neighbors) if they exist
        # This is where we would loop through self.context_data if fully implemented.
        # For now, we draw the single submap centered.
        
        # If we have context data (dictionary of submaps):
        # if self.context_data:
        #     for (dq, dr), submap in self.context_data.items():
        #         # Offset the drawing origin
        #         self.draw_single_submap(painter, center_x, center_y, submap, offset=(dq, dr))
        
        # Single submap drawing:
        # Calculate the width of a World Hex in pixels to center the submap correctly
        # A World Hex is rendered as the "Central" hex of the detail view.
        
        # Draw the sub-hexes
        h_step = self.dx
        v_step = self.dy
        
        # Draw the hexes from the SubMap object
        # self.map_data is the SubMap.hexes dictionary
        for p, h in self.map_data.items():
            q, r = p
            # Axial to Pixel for Pointy Top
            px = center_x + h_step * (q + r/2.0)
            py = center_y + v_step * r
            
            color = self.get_terrain_color(h.terrain, palette)
            poly = self.draw_hex_pointy(painter, QPointF(px, py), color)
            self.draw_terrain_icon(painter, QPointF(px, py), h.terrain)
            self.hex_hitboxes.append((poly, (None, q, r)))
            
        # Draw coordinate grid overlay (optional, matches screenshots)
        # Example: Draw a hexagon outline representing the Parent Hex boundary
        painter.setPen(QPen(QColor(255, 255, 255, 50), 2))
        # Radius of the 75-hex cluster is roughly 5 hex widths
        # Draw a large hexagon around the center
        # This visually confirms the boundary of the clicked hex
        pts = []
        for i in range(6):
            angle_deg = 60 * i - 90
            angle_rad = math.pi / 180 * angle_deg
            # Approximate radius for visual outline
            rad = 5 * self.dx 
            pts.append(QPointF(center_x + rad * math.cos(angle_rad), center_y + rad * math.sin(angle_rad)))
        painter.drawPolygon(QPolygonF(pts))

    def get_terrain_color(self, terrain, palette):
        # Priority order matches PDF
        if 'Starport' in terrain: return palette['Starport']
        if 'City' in terrain: return palette['City']
        if 'IceCap' in terrain: return palette['IceCap']
        if 'Ice Field' in terrain: return palette['Ice Field']
        if 'Ocean Depth' in terrain: return palette['Ocean Depth']
        if 'Abyss' in terrain: return palette['Abyss']
        if 'Ocean' in terrain: return palette['Ocean']
        if 'Mountain' in terrain: return palette['Mountain']
        if 'Shore' in terrain: return palette['Shore']
        if 'Islands' in terrain: return palette['Islands']
        if 'Desert' in terrain: return palette['Desert']
        if 'Crater' in terrain: return palette['Crater']
        if 'Woods' in terrain: return palette['Woods']
        if 'Cropland' in terrain: return palette['Cropland']
        if 'Rough' in terrain: return palette['Rough']
        return palette['Clear']

    def draw_terrain_icon(self, painter, center, terrain):
        icon = None
        if 'Mountain' in terrain: icon = self.icons['Mountain']
        elif 'City' in terrain: icon = self.icons['City']
        elif 'Starport' in terrain: icon = self.icons['Starport']
        
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
        
        order = ['IceCap', 'Ice Field', 'Mountain', 'Ocean', 'Shore', 'Islands', 'Desert', 'Rough', 'Woods', 'Cropland', 'Clear', 'City', 'Starport']
        return [t for t in order if t in visible]

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

# ... (WorldMapDialog remains largely the same, just passing context_data to widget)

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