"""
Shared utilities and miscellaneous views for StarBright.
Includes travel time calculators, QREBS generators/decoders, and the welcome screen.
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QGroupBox, QSpinBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPixmap

from travtools.travel import calculate_travel_time
import travtools.qrebs as qrebs_gen
from views.qt_components import Styles, GlassFrame

class TravelQtView(QWidget):
    """
    View for calculating interplanetary travel times based on distance and acceleration.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        frame = GlassFrame("Travel Time", "Calculate astronomical travel times", "#FF9800")
        
        self.adia_in = QLineEdit("100")
        self.pdia_in = QLineEdit("5000")
        self.spd_in = QLineEdit("1")
        
        btn = QPushButton("Calculate Time")
        btn.setStyleSheet("background-color: #E65100; color: white;")
        btn.clicked.connect(self.on_calculate)
        
        self.res_label = QLabel("Estimated travel time: -")
        self.res_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 20px; background: #000; border-radius: 8px;")
        self.res_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        frame.layout.addWidget(QLabel("Departure / Arrival Diameters (e.g. 100):"))
        frame.layout.addWidget(self.adia_in)
        frame.layout.addWidget(QLabel("Planet Diameter (km):"))
        frame.layout.addWidget(self.pdia_in)
        frame.layout.addWidget(QLabel("Ship Thrust (G):"))
        frame.layout.addWidget(self.spd_in)
        frame.layout.addWidget(btn)
        frame.layout.addWidget(self.res_label)
        
        layout.addWidget(frame)
        layout.addStretch()

    def on_calculate(self):
        try:
            a = float(self.adia_in.text())
            p = float(self.pdia_in.text())
            s = float(self.spd_in.text())
            hr, mins = calculate_travel_time(a, p, s)
            if hr is not None:
                self.res_label.setText(f"Estimated Time: {hr}h {mins}m")
                self.res_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 20px; background: #000; border-radius: 8px; color: #66BB6A;")
            else:
                self.res_label.setText("Invalid Parameters")
        except Exception as e:
            self.res_label.setText(f"Error: {e}")

class QrebsQtView(QWidget):
    """
    View for generating and decoding QREBS codes.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Generator
        gen_box = GlassFrame("QREBS Generator", color=Styles.PURPLE)
        rows_layout = QHBoxLayout()
        self.qty_spin = QSpinBox()
        self.qty_spin.setRange(1, 20)
        btn_gen = QPushButton("Generate")
        btn_gen.clicked.connect(self.on_generate)
        rows_layout.addWidget(QLabel("Quantity:"))
        rows_layout.addWidget(self.qty_spin)
        rows_layout.addWidget(btn_gen)
        
        self.gen_text = QTextEdit()
        self.gen_text.setReadOnly(True)
        self.gen_text.setStyleSheet(f"background: #000; color: {Styles.WHITE_TEXT};")
        
        gen_box.layout.addLayout(rows_layout)
        gen_box.layout.addWidget(self.gen_text)
        layout.addWidget(gen_box)
        
        # Decoder
        dec_box = GlassFrame("QREBS Decoder", color=Styles.TEAL)
        dec_layout = QHBoxLayout()
        self.dec_in = QLineEdit()
        self.dec_in.setPlaceholderText("5-char code")
        self.dec_in.setMaxLength(5)
        btn_dec = QPushButton("Decode")
        btn_dec.clicked.connect(self.on_decode)
        dec_layout.addWidget(self.dec_in)
        dec_layout.addWidget(btn_dec)
        
        self.dec_res = QLabel("Enter code to decode")
        self.dec_res.setWordWrap(True)
        self.dec_res.setStyleSheet("background: #000; padding: 10px; border-radius: 5px;")
        
        dec_box.layout.addLayout(dec_layout)
        dec_box.layout.addWidget(self.dec_res)
        layout.addWidget(dec_box)

    def on_generate(self):
        lines = []
        for _ in range(self.qty_spin.value()):
            res = qrebs_gen.generate_qrebs()
            lines.append(f"<font color='{Styles.CYAN}'><b>{res['code']}</b></font>: {res['text']}<br>")
        self.gen_text.setHtml("".join(lines))

    def on_decode(self):
        code = self.dec_in.text().upper()
        if len(code) != 5:
            self.dec_res.setText("Invalid Length")
            return
        res = qrebs_gen.decode_qrebs(code)
        self.dec_res.setText(res['text'])
        self.dec_res.setStyleSheet(f"background: #000; padding: 10px; border-radius: 5px; color: {Styles.GREEN if res['valid'] else 'red'};")

class WelcomeQtView(QWidget):
    """
    The initial welcome screen of the application, providing an overview of modules.
    """
    def __init__(self):
        super().__init__()
        self.bg_pixmap = QPixmap("assets/welcome_bg.png")
        self.init_ui()

    def paintEvent(self, event):
        painter = QPainter(self)
        if not self.bg_pixmap.isNull():
            # Scale pixmap to cover the whole widget
            scaled_bg = self.bg_pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
            # Center it
            x = (self.width() - scaled_bg.width()) // 2
            y = (self.height() - scaled_bg.height()) // 2
            painter.drawPixmap(x, y, scaled_bg)
        super().paintEvent(event)

    def init_ui(self):

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        container = GlassFrame("Welcome to StarBright", "Your definitive Traveller RPG companion", Styles.AMBER)
        container.setMinimumSize(600, 400)
        container.setStyleSheet(f"background-color: rgba(22, 27, 34, 0.7); border: 1px solid {Styles.BORDER_COLOR}; border-radius: 12px;")
        
        # Branding
        title = QLabel("STARBRIGHT")
        title.setStyleSheet(f"font-size: 72px; font-weight: 800; color: {Styles.AMBER}; letter-spacing: 15px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("ELECTRONIC DATA PROCESSING - TRAVELLER TOOLBOX")
        subtitle.setStyleSheet(f"font-size: 14px; color: {Styles.WHITE_TEXT}; letter-spacing: 2px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        info = QLabel(
            "Select a module from the menu bar above to begin.<br><br>"
            "<b>Galaxy Engine:</b> Generate stars and subsectors.<br>"
            "<b>Trading:</b> Buy and sell cargo across the stars.<br>"
            "<b>Makers:</b> Craft custom weaponry and armor.<br>"
            "<b>Utilities:</b> Dice, travel math, and more."
        )
        info.setStyleSheet(f"font-size: 16px; color: {Styles.WHITE_TEXT}; line-height: 1.6;")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setWordWrap(True)
        
        container.layout.addWidget(title)
        container.layout.addWidget(subtitle)
        container.layout.addSpacing(40)
        container.layout.addWidget(info)
        container.layout.addStretch()
        
        # Legal Disclaimer
        legal_text = (
            "The Traveller game in all forms is owned by Mongoose Publishing. "
            "Copyright 1977 – 2024 Mongoose Publishing. "
            "Traveller is a registered trademark of Mongoose Publishing."
        )
        legal_label = QLabel(legal_text)
        legal_label.setStyleSheet(f"color: {Styles.GREY_TEXT}; font-size: 10px; border: none; background: transparent;")
        legal_label.setWordWrap(True)
        legal_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container.layout.addWidget(legal_label)
        
        layout.addWidget(container)


