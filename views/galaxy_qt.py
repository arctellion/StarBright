from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QScrollArea, QFrame, QGridLayout, QSlider, QTableWidget, QTableWidgetItem, QHeaderView, QTextEdit, QStackedWidget
from PyQt6.QtCore import Qt, QPointF, QSize
from PyQt6.QtGui import QPainter, QPen, QColor, QPolygonF, QFont
import random
import math
import travtools.system as ts
import travtools.names as names
from views.qt_components import Styles, GlassFrame

class HexMapWidget(QWidget):
    def __init__(self, systems=None):
        super().__init__()
        self.systems = systems or []
        self.hex_radius = 35
        self.setMinimumSize(800, 800)


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

class SubsectorSummaryCard(QFrame):
    def __init__(self, letter, systems, on_click=None):
        super().__init__()
        self.letter = letter
        self.systems = systems
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
        
        self.letter_label = QLabel(f"Subsector {letter}")
        self.letter_label.setStyleSheet(f"color: {Styles.AMBER}; font-weight: bold; font-size: 14px; border: none;")
        
        count = len(systems)
        self.count_label = QLabel(f"{count} Systems")
        self.count_label.setStyleSheet("color: white; font-size: 12px; border: none;")
        
        layout.addWidget(self.letter_label)
        layout.addWidget(self.count_label)
        layout.addStretch()

    def mousePressEvent(self, event):
        if self.on_click:
            self.on_click(self.letter, self.systems)
        super().mousePressEvent(event)


class SystemQtView(QWidget):

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


    def on_generate_click(self):
        try:
            seed = int(self.seed_input.text() or 0)
            density = self.density_slider.value() / 10.0
            systems = ts.fun_subsector(seed, density)
            
            self.table.setRowCount(0)
            for s in systems:
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(s['name']))
                self.table.setItem(row, 1, QTableWidgetItem(s['coord']))
                uwp_item = QTableWidgetItem(s['uwp'])
                uwp_item.setForeground(Qt.GlobalColor.yellow)
                self.table.setItem(row, 2, uwp_item)
                self.table.setItem(row, 3, QTableWidgetItem(s['trade']))
            
            self.hex_map.set_systems(systems)

        except Exception as ex:
            print(f"Error generating subsector: {ex}")

class SectorQtView(QWidget):
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

    def on_card_click(self, letter, systems):
        self.detail_title.setText(f"Subsector {letter} Detail")
        
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


