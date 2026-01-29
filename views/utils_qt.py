from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QGroupBox, QSpinBox
from PyQt6.QtCore import Qt
from travtools.travel import calculate_travel_time
import travtools.qrebs as qrebs_gen
from views.qt_components import Styles, GlassFrame

class TravelQtView(QWidget):
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
