"""
PyQt6 views for galaxy exploration.
Contains widgets and views for generating individual star systems, 
subsectors, and sectors, including an interactive hex map.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                             QScrollArea, QFrame, QGridLayout, QSlider, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QTextEdit, QStackedWidget, QDialog, QComboBox)
from PyQt6.QtCore import Qt, QPointF, QPoint, QSize, pyqtSignal
from PyQt6.QtGui import QPainter, QPen, QColor, QPolygonF, QFont, QCursor
import random
import math
import travtools.system as ts
import travtools.names as names
import travtools.converters as cnv
from views.qt_components import Styles, GlassFrame

class HexMapWidget(QWidget):
    """
    A custom QWidget that renders an 8x10 hex grid and allows system selection.
    """
    systemSelected = pyqtSignal(dict)

    def __init__(self, systems=None):
        super().__init__()
        self.systems = systems or []
        self.hex_radius = 35
        self.setMinimumSize(800, 800)
        self.setMouseTracking(True)


    def set_systems(self, systems):
        self.systems = systems
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Background
        painter.fillRect(self.rect(), QColor("#000"))
        
        # Draw Hex Grid
        pen = QPen(QColor(Styles.BORDER_COLOR))
        pen.setWidth(1)
        painter.setPen(pen)
        
        for x in range(1, 9):
            for y in range(1, 11):
                center = self.hex_to_pixel(x, y)
                self.draw_hex(painter, center)
                
                # Draw Coord
                painter.setPen(QPen(QColor("#444")))
                painter.setFont(QFont("Arial", 7))
                painter.drawText(int(center.x()) - 10, int(center.y()) - 15, f"{x:02d}{y:02d}")
                painter.setPen(pen)

        # Draw Systems
        for s in self.systems:
            coord = s['coord']
            x = int(coord[:2])
            y = int(coord[2:])
            center = self.hex_to_pixel(x, y)
            
            # System Marker
            painter.setBrush(QColor(Styles.AMBER))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(center, 4, 4)
            
            # System Name
            painter.setPen(QPen(QColor(Styles.WHITE_TEXT)))
            painter.setFont(QFont("Arial", 8, QFont.Weight.Bold))
            name = s['name']
            metrics = painter.fontMetrics()
            name_width = metrics.horizontalAdvance(name)
            painter.drawText(int(center.x() - name_width/2), int(center.y() + 15), name)

    def hex_to_pixel(self, x, y):
        # Vertical hex layout
        # x is column, y is row
        width = math.sqrt(3) * self.hex_radius
        height = 2 * self.hex_radius
        
        px = x * width * 0.75 + 50
        py = y * height + 50
        
        # Offset every other column
        if x % 2 == 0:
            py += height / 2
            
        return QPointF(px, py)

    def draw_hex(self, painter, center):
        points = []
        for i in range(6):
            angle_deg = 60 * i
            angle_rad = math.pi / 180 * angle_deg
            points.append(QPointF(center.x() + self.hex_radius * math.cos(angle_rad),
                                 center.y() + self.hex_radius * math.sin(angle_rad)))
        
        painter.drawPolygon(QPolygonF(points))

    def mousePressEvent(self, event):
        # Determine which hex was clicked
        click_pos = event.position()
        
        best_dist = 20 # Click threshold
        selected_system = None
        
        for s in self.systems:
            coord = s['coord']
            x = int(coord[:2])
            y = int(coord[2:])
            center = self.hex_to_pixel(x, y)
            
            # Simple distance check from center of hex
            dist = math.sqrt((center.x() - click_pos.x())**2 + (center.y() - click_pos.y())**2)
            if dist < best_dist:
                selected_system = s
                break
        
        if selected_system:
            self.systemSelected.emit(selected_system)
        
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # Change cursor when hovering over a system
        hovering = False
        for s in self.systems:
            coord = s['coord']
            x = int(coord[:2])
            y = int(coord[2:])
            center = self.hex_to_pixel(x, y)
            dist = math.sqrt((center.x() - event.position().x())**2 + (center.y() - event.position().y())**2)
            if dist < 15:
                hovering = True
                break
        
        if hovering:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.unsetCursor()
        super().mouseMoveEvent(event)

class SystemDetailDialog(QDialog):
    """
    A dialog window that displays detailed information about a star system,
    including UWP breakdown and extended data.
    """
    def __init__(self, system, parent=None):
        super().__init__(parent)
        self.system = system
        self.setWindowTitle(f"System Details: {system['name']}")
        self.setMinimumWidth(500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.setStyleSheet(f"background-color: {Styles.BG_COLOR}; color: {Styles.WHITE_TEXT}; font-family: 'Segoe UI', sans-serif;")
        
        # Header
        header = GlassFrame(self.system['name'], f"Coordinates: {self.system['coord']}", Styles.AMBER)
        layout.addWidget(header)
        
        # UWP Breakdown
        uwp = self.system['uwp']
        uwp_frame = GlassFrame("Universal World Profile", uwp, Styles.BLUE)
        uwp_layout = QGridLayout()
        uwp_layout.setColumnStretch(1, 1)
        
        # UWP Parts: Sp Sz At Hy Po Go La - Tc
        # Indices:  0  1  2  3  4  5  6    8
        
        parts = [
            ("Starport", uwp[0], self.get_starport_desc(uwp[0])),
            ("Size", uwp[1], self.get_size_desc(uwp[1])),
            ("Atmosphere", uwp[2], self.get_atmo_desc(uwp[2])),
            ("Hydrographics", uwp[3], self.get_hydro_desc(uwp[3])),
            ("Population", uwp[4], self.get_pop_desc(uwp[4])),
            ("Government", uwp[5], self.get_gov_desc(uwp[5])),
            ("Law Level", uwp[6], self.get_law_desc(uwp[6])),
            ("Tech Level", uwp[8:], self.get_tech_desc(uwp[8:]))
        ]
        
        for i, (label, val, desc) in enumerate(parts):
            lbl_name = QLabel(f"<b>{label}:</b>")
            lbl_val = QLabel(f"<span style='color: {Styles.AMBER}; font-weight: bold;'>{val}</span>")
            lbl_desc = QLabel(f"<span style='color: {Styles.GREY_TEXT}; font-style: italic;'>{desc}</span>")
            
            uwp_layout.addWidget(lbl_name, i, 0)
            uwp_layout.addWidget(lbl_val, i, 1)
            uwp_layout.addWidget(lbl_desc, i, 2)
            
        uwp_frame.layout.addLayout(uwp_layout)
        layout.addWidget(uwp_frame)
        
        # Secondary Details (PBG, Bases, Trade, Ext)
        sec_frame = GlassFrame("Extended Data", "", Styles.GREEN)
        sec_layout = QVBoxLayout()
        
        sec_layout.addWidget(QLabel(f"<b>Stars:</b> <span style='color: {Styles.AMBER};'>{self.system.get('stars', 'Unknown')}</span>"))
        sec_layout.addWidget(QLabel(f"<b>Allegiance:</b> {self.system.get('allegiance', 'Unknown')}"))
        sec_layout.addWidget(QLabel(f"<b>PBG:</b> {self.system['pbg']} <span style='color: {Styles.GREY_TEXT}; ml-2'>(Pop Multiplier: {self.system['pbg'][0]}, Belts: {self.system['pbg'][1]}, Gas Giants: {self.system['pbg'][2]})</span>"))
        sec_layout.addWidget(QLabel(f"<b>Bases:</b> {self.get_bases_desc(self.system['bases'])}"))
        sec_layout.addWidget(QLabel(f"<b>Trade Classifications:</b> {self.system['trade']}"))
        sec_layout.addWidget(QLabel(f"<b>Importance & Economic:</b> {self.system['ext']}"))
        
        sec_frame.layout.addLayout(sec_layout)
        layout.addWidget(sec_frame)
        
        # All API Data (Scrollable)
        if 'raw_api_data' in self.system:
            raw_frame = GlassFrame("Detailed API Telemetry", "All available data from Traveller Map", Styles.GREY_TEXT)
            raw_scroll = QScrollArea()
            raw_scroll.setWidgetResizable(True)
            raw_scroll.setMaximumHeight(200)
            raw_scroll.setStyleSheet("background: #000; border: none;")
            
            raw_content = QWidget()
            raw_list = QVBoxLayout(raw_content)
            
            # Known fields to skip (already shown)
            skip = ['Name', 'Hex', 'UWP', 'PBG', 'Bases', 'Remarks', '{Ix}', '(Ex)', '[Cx]', 'Stars', 'Allegiance']
            
            for k, v in self.system['raw_api_data'].items():
                if k not in skip and v:
                    raw_list.addWidget(QLabel(f"<b>{k}:</b> {v}"))
            
            raw_scroll.setWidget(raw_content)
            raw_frame.layout.addWidget(raw_scroll)
            layout.addWidget(raw_frame)
        
        # Close button
        btn_close = QPushButton("Close")
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)

    def get_starport_desc(self, c):
        descs = {
            'A': "Excellent - Refined fuel, shipyard (Overhaul), base",
            'B': "Good - Refined fuel, shipyard (Repair), base",
            'C': "Routine - Unrefined fuel, shipyard (Small craft)",
            'D': "Poor - Unrefined fuel, no shipyard",
            'E': "Frontier - No fuel, no shipyard",
            'X': "No Starport"
        }
        return descs.get(c, "Unknown")
        
    def get_size_desc(self, c):
        val = cnv.ext_dec(c)
        if val == 0: return "Asteroid / Small Space Station"
        if val == 1: return "1,600 km (Triton)"
        if val == 2: return "3,200 km (Luna)"
        if val == 3: return "4,800 km (Mercury)"
        if val == 4: return "6,400 km (Mars)"
        if val == 5: return "8,000 km"
        if val == 6: return "9,600 km"
        if val == 7: return "11,200 km"
        if val == 8: return "12,800 km (Earth)"
        if val == 9: return "14,400 km"
        if val == 10: return "16,000 km"
        return f"{val*1600:,} km approx"

    def get_atmo_desc(self, c):
        val = cnv.ext_dec(c)
        descs = [
            "None / Vacuum", "Trace", "Very Thin, Tainted", "Very Thin",
            "Thin, Tainted", "Thin", "Standard", "Standard, Tainted",
            "Dense", "Dense, Tainted", "Exotic", "Corrosive",
            "Insidious", "Dense, High", "Ellipsoid", "Thin, Low"
        ]
        if val < len(descs): return descs[val]
        return "Special"

    def get_hydro_desc(self, c):
        val = cnv.ext_dec(c)
        if val == 0: return "Desert World (0%)"
        if val == 10: return "Water World (100%)"
        return f"Dry/Wet ({val*10}%)"

    def get_pop_desc(self, c):
        val = cnv.ext_dec(c)
        if val == 0: return "Unpopulated (Empty)"
        if val <= 3: return f"Small Colony (Hundreds/Thousands)"
        if val <= 6: return f"High Density Colony (Millions)"
        if val <= 8: return f"Planetary Civilization (Hundreds of Millions)"
        return f"Global Infrastructure (Billions+)"

    def get_gov_desc(self, c):
        val = cnv.ext_dec(c)
        descs = [
            "None / Anarchy", "Company/Corporation", "Participating Democracy", "Self-Perpetuating Oligarchy",
            "Representative Democracy", "Feudal Technocracy", "Captive Government", "Balkanized",
            "Civil Service Bureaucracy", "Impersonal Bureaucracy", "Charismatic Dictatorship", "Non-Charismatic Leader",
            "Charismatic Oligarchy", "Religious Dictatorship", "Religious Autocracy", "Totalitarian Oligarchy"
        ]
        if val < len(descs): return descs[val]
        return "Other"

    def get_law_desc(self, c):
        val = cnv.ext_dec(c)
        if val == 0: return "No Law (No weapons prohibited)"
        if val <= 3: return "Low Law (Heavy weapons restricted)"
        if val <= 6: return "Moderate Law (Open carry restricted)"
        if val <= 9: return "High Law (All firearms restricted)"
        return "Extreme Law (Everything restricted)"

    def get_tech_desc(self, c):
        val = cnv.ext_dec(c)
        if val <= 0: return "Stone Age"
        if val <= 3: return "Industrial (Pre-Space)"
        if val <= 8: return "Space Age / FTL Capable"
        if val <= 12: return "Advanced Space Age (Stellar)"
        return "High Tech (Galactic)"

    def get_bases_desc(self, b):
        if not b: return "None"
        parts = []
        if 'N' in b: parts.append("Naval Base")
        if 'S' in b: parts.append("Scout Base")
        if 'W' in b: parts.append("Way Station")
        if 'D' in b: parts.append("Depot")
        return ", ".join(parts)

class SubsectorSummaryCard(QFrame):
    """
    A small card widget showing a summary of a subsector, used in the Sector view grid.
    """
    def __init__(self, letter, systems, name=None, on_click=None):
        super().__init__()
        self.letter = letter
        self.systems = systems
        self.name = name or f"Subsector {letter}"
        self.on_click = on_click
        self.setObjectName("SubsectorSummaryCard")

        self.setStyleSheet(f"""
            SubsectorSummaryCard {{
                border: 1px solid {Styles.BORDER_COLOR};
                border-radius: 8px;
                background: rgba(20, 20, 20, 0.8);
                padding: 10px;
            }}
            SubsectorSummaryCard:hover {{
                background: rgba(40, 40, 40, 0.9);
                border-color: {Styles.AMBER};
            }}
        """)
        layout = QVBoxLayout(self)
        
        self.letter_label = QLabel(self.name)
        self.letter_label.setStyleSheet(f"color: {Styles.AMBER}; font-weight: bold; font-size: 14px; border: none;")
        
        count = len(systems)
        self.count_label = QLabel(f"{count} Systems")
        self.count_label.setStyleSheet("color: white; font-size: 12px; border: none;")
        
        layout.addWidget(self.letter_label)
        layout.addWidget(self.count_label)
        layout.addStretch()

    def mousePressEvent(self, event):
        if self.on_click:
            self.on_click(self.letter, self.systems, self.name)
        super().mousePressEvent(event)


class SystemQtView(QWidget):
    """
    View for generating and viewing a single star system.
    """

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        frame = GlassFrame("System Generator", "Generate individual star systems", Styles.AMBER)
        
        input_layout = QHBoxLayout()
        self.seed_input = QLineEdit("12345")
        self.seed_input.setPlaceholderText("Enter seed (numeric)")
        
        btn_random = QPushButton("Random")
        btn_random.clicked.connect(self.on_random_click)
        
        btn_generate = QPushButton("Generate")
        btn_generate.clicked.connect(self.on_generate_click)
        
        input_layout.addWidget(self.seed_input)
        input_layout.addWidget(btn_random)
        input_layout.addWidget(btn_generate)
        
        self.result_frame = QFrame()
        self.result_frame.setStyleSheet(f"border: 1px solid {Styles.BORDER_COLOR}; border-radius: 8px; background: #000; padding: 15px;")
        self.result_layout = QVBoxLayout(self.result_frame)
        
        self.uwp_label = QLabel("UWP: -")
        self.uwp_label.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {Styles.AMBER};")
        
        self.details_label = QLabel("")
        self.details_label.setStyleSheet(f"font-size: 16px; color: {Styles.WHITE_TEXT};")
        self.details_label.setWordWrap(True)
        
        self.result_layout.addWidget(self.uwp_label)
        self.result_layout.addWidget(self.details_label)
        self.result_layout.addStretch()
        
        frame.layout.addLayout(input_layout)
        frame.layout.addWidget(self.result_frame)
        
        layout.addWidget(frame)
        layout.addStretch()

    def on_random_click(self):
        self.seed_input.setText(str(random.randint(1000, 999999)))

    def on_generate_click(self):
        try:
            seed = int(self.seed_input.text() or 0)
            uwp = ts.fun_uwp(seed)
            pbg = ts.fun_pbg(uwp)
            bases = ts.fun_bases(uwp)
            trade = ts.fun_trade(uwp)
            ext = ts.fun_ext(uwp, pbg, bases, trade)
            
            planet_name = names.generate_planet_name("0000", uwp)
            
            self.uwp_label.setText(f"{planet_name} [{uwp}]")
            details = f"<b>PBG:</b> {pbg}<br><b>Bases:</b> {bases if bases else 'None'}<br><b>Trade:</b> {trade}<br><b>Extensions:</b> {ext}"
            self.details_label.setText(details)
        except Exception as ex:
            self.uwp_label.setText("Error")
            self.details_label.setText(str(ex))

class SubsectorQtView(QWidget):
    """
    View for generating and viewing an 8x10 subsector.
    Includes a table of systems and an interactive hex map.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        frame = GlassFrame("Subsector Generator", "8x10 Hex Grid generation", Styles.AMBER)
        
        input_layout = QHBoxLayout()
        self.seed_input = QLineEdit("67890")
        
        self.density_slider = QSlider(Qt.Orientation.Horizontal)
        self.density_slider.setRange(1, 10)
        self.density_slider.setValue(5)
        
        btn_generate = QPushButton("Generate Subsector")
        btn_generate.clicked.connect(self.on_generate_click)
        
        input_layout.addWidget(QLabel("Seed:"))
        input_layout.addWidget(self.seed_input)
        input_layout.addWidget(QLabel("Density:"))
        input_layout.addWidget(self.density_slider)
        input_layout.addWidget(btn_generate)
        
        main_content = QHBoxLayout()
        
        # Left side: Table
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Name", "Coord", "UWP", "Trade Codes"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet(f"background-color: #000; gridline-color: {Styles.BORDER_COLOR}; color: {Styles.WHITE_TEXT};")
        self.table.setMaximumWidth(400)
        
        # Right side: Hex Map
        self.map_scroll = QScrollArea()
        self.hex_map = HexMapWidget()
        self.map_scroll.setWidget(self.hex_map)
        self.map_scroll.setWidgetResizable(True)
        self.map_scroll.setStyleSheet(f"border: 1px solid {Styles.BORDER_COLOR}; background: #000;")
        
        main_content.addWidget(self.table, 1)
        main_content.addWidget(self.map_scroll, 2)
        
        frame.layout.addLayout(input_layout)
        frame.layout.addLayout(main_content)
        
        layout.addWidget(frame)

        # Connections
        self.hex_map.systemSelected.connect(self.show_system_details)
        self.table.itemDoubleClicked.connect(self.on_table_double_click)
        self.table.verticalHeader().sectionClicked.connect(self.on_row_header_click)


    def on_generate_click(self):
        try:
            seed = int(self.seed_input.text() or 0)
            density = self.density_slider.value() / 10.0
            self.current_systems = ts.fun_subsector(seed, density)
            
            self.table.setRowCount(0)
            for s in self.current_systems:
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(s['name']))
                self.table.setItem(row, 1, QTableWidgetItem(s['coord']))
                uwp_item = QTableWidgetItem(s['uwp'])
                uwp_item.setForeground(Qt.GlobalColor.yellow)
                self.table.setItem(row, 2, uwp_item)
                self.table.setItem(row, 3, QTableWidgetItem(s['trade']))
            
            self.hex_map.set_systems(self.current_systems)

        except Exception as ex:
            print(f"Error generating subsector: {ex}")

    def on_table_double_click(self, item):
        row = item.row()
        if hasattr(self, 'current_systems') and row < len(self.current_systems):
            self.show_system_details(self.current_systems[row])

    def on_row_header_click(self, row):
        if hasattr(self, 'current_systems') and row < len(self.current_systems):
            self.show_system_details(self.current_systems[row])

    def show_system_details(self, system):
        dialog = SystemDetailDialog(system, self)
        dialog.exec()

class SectorQtView(QWidget):
    """
    View for generating and viewing a full 16-subsector sector.
    Allows drilling down into individual subsectors.
    """
    def __init__(self):
        super().__init__()
        self.sector_data = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.main_frame = GlassFrame("Sector Generator", "Complete Sector (16 Subsectors)", Styles.AMBER)
        
        input_layout = QHBoxLayout()
        self.seed_input = QLineEdit("55555")
        
        self.density_slider = QSlider(Qt.Orientation.Horizontal)
        self.density_slider.setRange(1, 10)
        self.density_slider.setValue(5)
        
        btn_generate = QPushButton("Generate Sector")
        btn_generate.clicked.connect(self.on_generate_click)
        
        input_layout.addWidget(QLabel("Seed:"))
        input_layout.addWidget(self.seed_input)
        input_layout.addWidget(QLabel("Density:"))
        input_layout.addWidget(self.density_slider)
        input_layout.addWidget(btn_generate)
        
        # Stacked Widget for Grid vs Detail
        self.stack = QStackedWidget()
        
        # Page 1: Grid
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(f"background-color: #000; border: 1px solid {Styles.BORDER_COLOR};")
        
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(10)
        self.scroll_area.setWidget(self.grid_container)
        self.stack.addWidget(self.scroll_area)
        
        # Page 2: Detail
        self.detail_widget = QWidget()
        self.detail_layout = QVBoxLayout(self.detail_widget)
        
        detail_header = QHBoxLayout()
        self.detail_title = QLabel("Subsector Detail")
        self.detail_title.setStyleSheet(f"color: {Styles.AMBER}; font-size: 20px; font-weight: bold;")
        btn_back = QPushButton("Back to Sector")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_back.setFixedWidth(120)
        detail_header.addWidget(self.detail_title)
        detail_header.addStretch()
        detail_header.addWidget(btn_back)
        
        detail_content = QHBoxLayout()
        
        # Detail Table
        self.detail_table = QTableWidget(0, 4)
        self.detail_table.setHorizontalHeaderLabels(["Name", "Coord", "UWP", "Trade Codes"])
        self.detail_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.detail_table.setStyleSheet(f"background-color: #000; gridline-color: {Styles.BORDER_COLOR}; color: {Styles.WHITE_TEXT};")
        self.detail_table.setMaximumWidth(400)
        
        # Detail Map
        self.detail_map_scroll = QScrollArea()
        self.detail_map = HexMapWidget()
        self.detail_map_scroll.setWidget(self.detail_map)
        self.detail_map_scroll.setWidgetResizable(True)
        self.detail_map_scroll.setStyleSheet(f"border: 1px solid {Styles.BORDER_COLOR}; background: #000;")
        
        detail_content.addWidget(self.detail_table, 1)
        detail_content.addWidget(self.detail_map_scroll, 2)
        
        self.detail_layout.addLayout(detail_header)
        self.detail_layout.addLayout(detail_content)
        self.stack.addWidget(self.detail_widget)
        
        self.main_frame.layout.addLayout(input_layout)
        self.main_frame.layout.addWidget(self.stack)
        
        layout.addWidget(self.main_frame)

        # Connections
        self.detail_map.systemSelected.connect(self.show_system_details)
        self.detail_table.itemDoubleClicked.connect(self.on_table_double_click)
        self.detail_table.verticalHeader().sectionClicked.connect(self.on_row_header_click)


    def on_generate_click(self):
        try:
            # Clear previous grid
            for i in reversed(range(self.grid_layout.count())): 
                widget = self.grid_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)

            seed = int(self.seed_input.text() or 0)
            density = self.density_slider.value() / 10.0
            self.sector_data = ts.fun_sector(seed, density)
            
            # Subsectors are A-P (16 total)
            # Layout in a 4x4 grid
            names = "ABCDEFGHIJKLMNOP"
            for i, letter in enumerate(names):
                row = i // 4
                col = i % 4
                systems = self.sector_data.get(letter, [])
                card = SubsectorSummaryCard(letter, systems, self.on_card_click)
                self.grid_layout.addWidget(card, row, col)
            
            self.stack.setCurrentIndex(0) # Ensure grid is visible
                
        except Exception as ex:
            print(f"Error generating sector: {ex}")

    def on_table_double_click(self, item):
        row = item.row()
        if hasattr(self, 'current_detail_systems') and row < len(self.current_detail_systems):
            self.show_system_details(self.current_detail_systems[row])

    def on_row_header_click(self, row):
        if hasattr(self, 'current_detail_systems') and row < len(self.current_detail_systems):
            self.show_system_details(self.current_detail_systems[row])

    def show_system_details(self, system):
        dialog = SystemDetailDialog(system, self)
        dialog.exec()

    def on_card_click(self, letter, systems):
        self.detail_title.setText(f"Subsector {letter} Detail")
        self.current_detail_systems = systems
        
        # Populate table
        self.detail_table.setRowCount(0)
        for s in systems:
            row = self.detail_table.rowCount()
            self.detail_table.insertRow(row)
            self.detail_table.setItem(row, 0, QTableWidgetItem(s['name']))
            self.detail_table.setItem(row, 1, QTableWidgetItem(s['coord']))
            uwp_item = QTableWidgetItem(s['uwp'])
            uwp_item.setForeground(Qt.GlobalColor.yellow)
            self.detail_table.setItem(row, 2, uwp_item)
            self.detail_table.setItem(row, 3, QTableWidgetItem(s['trade']))
            
        # Update map
        self.detail_map.set_systems(systems)
        
        # Switch to detail page
        self.stack.setCurrentIndex(1)



class TravellerMapQtView(QWidget):
    """
    Enhanced View for Traveller Map API using official Milieu and Sector lists.
    """
    def __init__(self):
        super().__init__()
        import travtools.traveller_map_api as tmap
        self.tmap = tmap
        self.metadata = self.load_metadata()
        self.ss_names = {} # Map Index -> Name
        self.init_ui()
        self.populate_milieux()

    def _load_metadata_internal(self):
        import os
        import json
        json_path = os.path.join(os.path.dirname(__file__), '..', 'travtools', 'traveller_map_data.json')
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading traveller map metadata: {e}")
            return {"milieux": [], "sectors": {}}

    def load_metadata(self):
        # Alias for consistency if needed, but the method above is fine
        return self._load_metadata_internal()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        frame = GlassFrame("Traveller Map Viewer", "Official Sectors from travellermap.com", Styles.BLUE)
        
        input_layout = QHBoxLayout()
        self.milieu_combo = QComboBox()
        self.sector_combo = QComboBox()
        self.sector_combo.setEditable(True)
        self.sector_combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.sector_combo.completer().setFilterMode(Qt.MatchFlag.MatchContains)
        
        btn_clear = QPushButton("Clear")
        btn_clear.setFixedWidth(60)
        btn_clear.clicked.connect(self.populate_milieux)

        btn_load = QPushButton("Fetch Sector Data")
        btn_load.clicked.connect(self.on_load_click)
        
        self.milieu_combo.currentIndexChanged.connect(self.on_milieu_change)
        
        input_layout.addWidget(QLabel("Milieu:"))
        input_layout.addWidget(self.milieu_combo)
        input_layout.addWidget(QLabel("Sector:"))
        input_layout.addWidget(self.sector_combo, 1)
        input_layout.addWidget(btn_clear)
        input_layout.addWidget(btn_load)
        
        # Main content areas (Stacked)
        self.stack = QStackedWidget()
        
        # Page 1: Sector Grid View
        self.grid_scroll = QScrollArea()
        self.grid_scroll.setWidgetResizable(True)
        self.grid_scroll.setStyleSheet(f"background-color: #000; border: 1px solid {Styles.BORDER_COLOR};")
        
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(10)
        self.grid_scroll.setWidget(self.grid_container)
        self.stack.addWidget(self.grid_scroll)
        
        # Page 2: Subsector Detail View
        self.detail_widget = QWidget()
        self.detail_layout = QVBoxLayout(self.detail_widget)
        
        detail_header = QHBoxLayout()
        self.detail_title = QLabel("Subsector Detail")
        self.detail_title.setStyleSheet(f"color: {Styles.BLUE}; font-size: 20px; font-weight: bold;")
        btn_back = QPushButton("Back to Sector View")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_back.setFixedWidth(150)
        detail_header.addWidget(self.detail_title)
        detail_header.addStretch()
        detail_header.addWidget(btn_back)
        
        detail_content = QHBoxLayout()
        
        # Left side: Table
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Name", "Coord", "UWP", "Remarks"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet(f"background-color: #000; gridline-color: {Styles.BORDER_COLOR}; color: {Styles.WHITE_TEXT};")
        self.table.setMaximumWidth(400)
        
        # Right side: Hex Map
        self.map_scroll = QScrollArea()
        self.hex_map = HexMapWidget()
        self.map_scroll.setWidget(self.hex_map)
        self.map_scroll.setWidgetResizable(True)
        self.map_scroll.setStyleSheet(f"border: 1px solid {Styles.BORDER_COLOR}; background: #000;")
        
        detail_content.addWidget(self.table, 1)
        detail_content.addWidget(self.map_scroll, 2)
        
        self.detail_layout.addLayout(detail_header)
        self.detail_layout.addLayout(detail_content)
        self.stack.addWidget(self.detail_widget)
        
        frame.layout.addLayout(input_layout)
        frame.layout.addWidget(self.stack)
        
        layout.addWidget(frame)

        # Connections
        self.hex_map.systemSelected.connect(self.show_system_details)
        self.table.itemDoubleClicked.connect(self.on_table_double_click)
        self.table.verticalHeader().sectionClicked.connect(self.on_row_header_click)

    def populate_milieux(self):
        self.milieu_combo.clear()
        self.milieu_combo.addItem("Select Milieu...", None)
        for m in self.metadata.get("milieux", []):
            self.milieu_combo.addItem(f"{m['Name']} ({m['Code']})", m['Code'])
        
        # Reset sectors
        self.sector_combo.clear()
        self.sector_combo.addItem("Select Sector...", None)
        
        # Clear data and grid
        self.full_sector_systems = []
        for i in reversed(range(self.grid_layout.count())): 
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        self.stack.setCurrentIndex(0)

    def on_milieu_change(self):
        milieu_code = self.milieu_combo.currentData()
        self.sector_combo.clear()
        self.sector_combo.addItem("Select Sector...", None)
        
        if not milieu_code:
            return

        if milieu_code in self.metadata.get("sectors", {}):
            sectors = self.metadata["sectors"][milieu_code]
            
            # Sort sectors alphabetically by name
            def get_name(s):
                name = s['Names'][0]['Text']
                for n in s['Names']:
                    if 'Lang' not in n or n['Lang'] == 'en':
                        return n['Text']
                return name
            
            sorted_sectors = sorted(sectors, key=get_name)
            
            for s in sorted_sectors:
                self.sector_combo.addItem(get_name(s), s['Abbreviation'])
        
        # Reset search/text
        self.sector_combo.setEditText("")

    def on_load_click(self):
        milieu = self.milieu_combo.currentData()
        sector_name = self.sector_combo.currentText()
        if not milieu or sector_name == "Select Sector...":
            return

        # Fetch system data
        tab_data = self.tmap.fetch_sector_tab_data(milieu, sector_name)
        if tab_data:
            self.full_sector_systems = self.tmap.parse_tab_data(tab_data)
            self.sector_abbr = self.sector_combo.currentData()
            self.sector_display_name = sector_name
            
            # Fetch sector metadata for subsector names
            self.ss_names = {}
            meta = self.tmap.fetch_sector_metadata(milieu, sector_name)
            if meta and "Subsectors" in meta:
                for ss in meta["Subsectors"]:
                    idx = ss.get("Index")
                    name = ss.get("Name")
                    if idx and name:
                        self.ss_names[idx] = name
            
            self.render_sector_grid()
            self.stack.setCurrentIndex(0)
        else:
            print(f"Failed to load TabDelimited data for {sector_name}")

    def render_sector_grid(self):
        # Clear previous grid
        for i in reversed(range(self.grid_layout.count())): 
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        # Group systems by subsector (A-P)
        ss_map = {}
        for s in self.full_sector_systems:
            ss = s.get('subsector', ' ')
            if ss not in ss_map: ss_map[ss] = []
            ss_map[ss].append(s)
            
        names = "ABCDEFGHIJKLMNOP"
        for i, letter in enumerate(names):
            row = i // 4
            col = i % 4
            systems = ss_map.get(letter, [])
            ss_name = self.ss_names.get(letter)
            card = SubsectorSummaryCard(letter, systems, name=ss_name, on_click=self.on_card_click)
            self.grid_layout.addWidget(card, row, col)

    def on_card_click(self, letter, systems, ss_name):
        display_name = ss_name if ss_name else f"Subsector {letter}"
        self.detail_title.setText(f"{self.sector_display_name} - {display_name}")
        self.current_systems = systems
        self.update_display()
        self.stack.setCurrentIndex(1)

    def update_display(self):
        self.table.setRowCount(0)
        for s in self.current_systems:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(s['name']))
            self.table.setItem(row, 1, QTableWidgetItem(s['coord']))
            uwp_item = QTableWidgetItem(s['uwp'])
            uwp_item.setForeground(Qt.GlobalColor.yellow)
            self.table.setItem(row, 2, uwp_item)
            self.table.setItem(row, 3, QTableWidgetItem(s['trade']))
        
        self.hex_map.set_systems(self.current_systems)

    def on_table_double_click(self, item):
        row = item.row()
        if hasattr(self, 'current_systems') and row < len(self.current_systems):
            self.show_system_details(self.current_systems[row])

    def on_row_header_click(self, row):
        if hasattr(self, 'current_systems') and row < len(self.current_systems):
            self.show_system_details(self.current_systems[row])

    def show_system_details(self, system):
        dialog = SystemDetailDialog(system, self)
        dialog.exec()
