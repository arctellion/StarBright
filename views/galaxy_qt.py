from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QScrollArea, QFrame, QGridLayout, QSlider, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
import random
import travtools.system as ts
from views.qt_components import Styles, GlassFrame

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
            
            self.uwp_label.setText(f"UWP: {uwp}")
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
        
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Coord", "UWP", "Trade Codes"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet(f"background-color: #000; gridline-color: {Styles.BORDER_COLOR}; color: {Styles.WHITE_TEXT};")
        
        frame.layout.addLayout(input_layout)
        frame.layout.addWidget(self.table)
        
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
                self.table.setItem(row, 0, QTableWidgetItem(s['coord']))
                uwp_item = QTableWidgetItem(s['uwp'])
                uwp_item.setForeground(Qt.GlobalColor.yellow)
                self.table.setItem(row, 1, uwp_item)
                self.table.setItem(row, 2, QTableWidgetItem(s['trade']))
        except Exception as ex:
            print(f"Error generating subsector: {ex}")

class SectorQtView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        frame = GlassFrame("Sector Generator", "Complete Sector (16 Subsectors)", Styles.AMBER)
        
        input_layout = QHBoxLayout()
        self.seed_input = QLineEdit("55555")
        btn_generate = QPushButton("Generate Sector")
        btn_generate.clicked.connect(self.on_generate_click)
        
        input_layout.addWidget(QLabel("Seed:"))
        input_layout.addWidget(self.seed_input)
        input_layout.addWidget(btn_generate)
        
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.result_area.setStyleSheet(f"background-color: #000; color: {Styles.WHITE_TEXT}; border: 1px solid {Styles.BORDER_COLOR};")
        
        frame.layout.addLayout(input_layout)
        frame.layout.addWidget(self.result_area)
        
        layout.addWidget(frame)

    def on_generate_click(self):
        try:
            seed = int(self.seed_input.text() or 0)
            sector_data = ts.fun_sector(seed)
            
            summary = []
            for name, systems in sector_data.items():
                summary.append(f"<b>Subsector {name}</b>: {len(systems)} systems")
                for s in systems[:3]: # Show first 3 systems as example
                    summary.append(f"  {s['coord']} {s['uwp']} {s['trade']}")
                summary.append("  ...")
            
            self.result_area.setHtml("<br>".join(summary))
        except Exception as ex:
            self.result_area.setText(str(ex))
