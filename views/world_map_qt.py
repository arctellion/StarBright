from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QScrollArea, QWidget)
from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import QPainter, QPen, QColor, QPolygonF, QFont, QBrush
from views.qt_components import Styles, GlassFrame
import math

class WorldMapWidget(QWidget):
    def __init__(self, map_data, size):
        super().__init__()
        self.map_data = map_data
        self.world_size = size
        
        # Base scaling logic
        self.scale = 1.0
        if size > 15: self.scale = 0.5
        elif size > 10: self.scale = 0.7
        elif size > 6: self.scale = 0.85
        
        # Calculate bounding box for the net
        # Each triangle base is S * 32
        # 5 triangles wide
        mw = 5 * size * 32 + 200
        mh = 4 * size * 28 + 300
        self.setMinimumSize(int(mw * self.scale), int(mh * self.scale))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#1a1a1a"))
        
        painter.scale(self.scale, self.scale)
        
        # Palette: Vibrant and distinct
        palette = {
            'Ocean': QColor("#2b6cb0"), # Strong Blue
            'Clear': QColor("#689f38"), # Grass Green
            'Mountain': QColor("#5d4037"), # Rock Brown
            'IceCap': QColor("#eceff1"), # Snow White
            'Desert': QColor("#edc9af"), # Sand
            'Equator': QColor(Styles.AMBER),
            'Grid': QColor("rgba(255, 255, 255, 30)")
        }

        map_left = 60
        map_top = 40

        for tri in self.map_data:
            tid = tri['id']
            up_or_down = tri['up_or_down']
            large_or_small = tri['large_or_small']
            base_idx = tid // 4
            vert_pos = tid % 4
            
            # Precise T5-style icosahedral net projection offsets from world_mapping.js
            if vert_pos == 0: # SMALL UP
                tl = map_left + 16 + (base_idx * self.world_size * 32)
                tt = map_top
            elif vert_pos == 1: # LARGE DOWN
                tl = map_left + 16 + (base_idx * self.world_size * 32)
                tt = map_top + (self.world_size - 2) * 28
            elif vert_pos == 2: # LARGE UP
                tl = map_left + self.world_size * 16 + base_idx * self.world_size * 32
                tt = map_top + self.world_size * 28
            else: # SMALL DOWN (vert_pos 3)
                tl = map_left + self.world_size * 16 + base_idx * self.world_size * 32 + 32
                tt = map_top + (self.world_size * 2) * 28 - 28

            h_side = self.world_size if large_or_small == 1 else self.world_size - 1

            for h in tri['hexes']:
                if up_or_down == 0: # UP
                    hx = tl + h['x'] * 32 + (h_side - h['y']) * 16
                    hy = tt + h['y'] * 28
                else: # DOWN
                    hx = tl + h['x'] * 32 + h['y'] * 16
                    hy = tt + (h['y'] + 1) * 28

                color = palette['Clear']
                if 'IceCap' in h['terrain']: color = palette['IceCap']
                elif 'Ocean' in h['terrain']: color = palette['Ocean']
                elif 'Mountain' in h['terrain']: color = palette['Mountain']
                elif 'Desert' in h['terrain']: color = palette['Desert']
                
                self.draw_hex(painter, QPointF(hx, hy), color)
        
        # Equator (Approximate mid-line)
        # In T5 it usually passes through the middle of the belt triangles
        eq_y = map_top + (self.world_size * 1.5) * 28
        painter.setPen(QPen(palette['Equator'], 2, Qt.PenStyle.DashLine))
        total_w = (5 * self.world_size * 32 + 100)
        painter.drawLine(0, int(eq_y), int(total_w), int(eq_y))

    def draw_hex(self, painter, center, color):
        # T5 Stretched Hex Geometry:
        # Width: 32px, Height: 35px, Vertical Step: 28px
        # Coordinates relative to top-left of hex bounding box
        x, y = center.x(), center.y()
        points = [
            QPointF(x + 16, y),
            QPointF(x + 32, y + 7),
            QPointF(x + 32, y + 28),
            QPointF(x + 16, y + 35),
            QPointF(x + 0, y + 28),
            QPointF(x + 0, y + 7)
        ]
        
        painter.setBrush(color)
        painter.setPen(QPen(QColor(0, 0, 0, 80), 0.5))
        painter.drawPolygon(QPolygonF(points))

class WorldMapDialog(QDialog):
    def __init__(self, world_name, uwp, map_data, size, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Stellar Cartography: {world_name}")
        self.resize(1200, 900)
        self.init_ui(world_name, uwp, map_data, size)

    def init_ui(self, world_name, uwp, map_data, size):
        layout = QVBoxLayout(self)
        self.setStyleSheet(f"background-color: {Styles.BG_COLOR}; color: white;")
        
        # Sample-like header
        header = QFrame()
        header.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #222, stop:1 #111); border-bottom: 2px solid #555; padding: 10px;")
        h_layout = QVBoxLayout(header)
        
        title = QLabel(f"<span style='font-size: 24px; font-weight: bold; color: {Styles.AMBER};'>{world_name}</span>")
        uwp_lbl = QLabel(f"<span style='font-size: 16px; color: #aaa;'>UNIVERSAL WORLD PROFILE: </span><span style='font-size: 18px; color: white;'>{uwp}</span>")
        h_layout.addWidget(title)
        h_layout.addWidget(uwp_lbl)
        layout.addWidget(header)

        # Mapping Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: #000; border: none;")
        self.map_widget = WorldMapWidget(map_data, size)
        scroll.setWidget(self.map_widget)
        layout.addWidget(scroll)

        # Legend and Stats
        legend = QHBoxLayout()
        lands = sum(1 for t in map_data for h in t['hexes'] if 'Ocean' not in h['terrain'])
        total = sum(1 for t in map_data for h in t['hexes'])
        perc = (lands / total * 100) if total > 0 else 0
        
        stats_lbl = QLabel(f"<b>Surface Integrity:</b> {perc:.1f}% Landmass | {total} Mapping Sectors")
        stats_lbl.setStyleSheet(f"color: {Styles.GREY_TEXT}; padding: 10px;")
        legend.addWidget(stats_lbl)
        legend.addStretch()
        
        btn_close = QPushButton("Return to Orbital Control")
        btn_close.clicked.connect(self.close)
        btn_close.setFixedSize(200, 40)
        btn_close.setStyleSheet(f"background-color: {Styles.BLUE}; font-weight: bold; border-radius: 5px;")
        legend.addWidget(btn_close)
        layout.addLayout(legend)
