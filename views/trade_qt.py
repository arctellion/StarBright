from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, QScrollArea, QFrame, QTextEdit
from PyQt6.QtCore import Qt
import re
import travtools.commerce as cm
from views.qt_components import Styles, GlassFrame, NumericSpinner

class BuyQtView(QWidget):
    def __init__(self):
        super().__init__()
        self.uwp_pat = re.compile('[ABCDEXFGHY][0-9A-F][0-9A-F][0-9A][0-9A-F][0-9A-F][0-9A-J]-[0-9A-J]')
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        frame = GlassFrame("Speculative Trade: Buy", "Find goods available for purchase", Styles.BLUE)
        
        self.uwp_input = QLineEdit()
        self.uwp_input.setPlaceholderText("UWP (e.g., A110877-E)")
        
        self.days_spinner = NumericSpinner("Days", value=7, min_val=1, max_val=14)
        
        # Skills
        skill_layout = QVBoxLayout()
        self.steward = NumericSpinner("Steward", value=0)
        self.admin = NumericSpinner("Admin", value=0)
        self.streetwise = NumericSpinner("Streetwise", value=0)
        self.liaison = NumericSpinner("Liaison", value=0)
        
        skill_layout.addLayout(self.steward)
        skill_layout.addLayout(self.admin)
        skill_layout.addLayout(self.streetwise)
        skill_layout.addLayout(self.liaison)
        
        self.btn_generate = QPushButton("Generate Goods")
        self.btn_generate.clicked.connect(self.on_buy_click)
        
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.result_area.setStyleSheet(f"background-color: #000; color: {Styles.BLUE}; border: 1px solid {Styles.BLUE}; border-radius: 8px; padding: 10px;")
        
        frame.layout.addWidget(QLabel("Current Location UWP:"))
        frame.layout.addWidget(self.uwp_input)
        frame.layout.addLayout(self.days_spinner)
        frame.layout.addWidget(QLabel("Character Skills:"))
        frame.layout.addLayout(skill_layout)
        frame.layout.addWidget(self.btn_generate)
        frame.layout.addWidget(QLabel("Results:"))
        frame.layout.addWidget(self.result_area)
        
        layout.addWidget(frame)
        layout.addStretch()

    def on_buy_click(self):
        uwp = self.uwp_input.text().upper()
        if not uwp:
            self.result_area.setText("Error: No UWP Provided.")
            return
        if not self.uwp_pat.match(uwp):
            self.result_area.setText("Error: Incorrect UWP pattern.")
            return
            
        try:
            skills = {
                'Steward': self.steward.value, 
                'Admin': self.admin.value, 
                'Streetwise': self.streetwise.value, 
                'Liaison': self.liaison.value
            }
            trade_data = cm.trade_gds(uwp, skills, self.days_spinner.value)
            self.result_area.setText(trade_data if trade_data else "No goods found.")
        except Exception as ex:
            self.result_area.setText(f"Error: {str(ex)}")

class SellQtView(QWidget):
    def __init__(self):
        super().__init__()
        self.uwp_pat = re.compile('[ABCDEXFGHY][0-9A-F][0-9A-F][0-9A][0-9A-F][0-9A-F][0-9A-J]-[0-9A-J]')
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        frame = GlassFrame("Speculative Trade: Sell", "Determine sale price for cargo", Styles.GREEN)
        
        self.cargo_input = QLineEdit()
        self.cargo_input.setPlaceholderText("Cargo ID (e.g., B - Ri Cr5,100)")
        
        self.uwp_input = QLineEdit()
        self.uwp_input.setPlaceholderText("Destination UWP")
        
        # Broker Skill
        broker_layout = QHBoxLayout()
        broker_layout.addWidget(QLabel("Broker Skill:"))
        self.broker_skill = QComboBox()
        self.broker_skill.addItems([str(i) for i in range(16)])
        broker_layout.addWidget(self.broker_skill)
        
        # Trade Roll
        trade_layout = QHBoxLayout()
        trade_layout.addWidget(QLabel("Trade pre-roll (optional):"))
        self.trade_roll = QComboBox()
        self.trade_roll.addItems([str(i) for i in range(7)])
        trade_layout.addWidget(self.trade_roll)
        
        self.btn_calculate = QPushButton("Calculate Sale Price")
        self.btn_calculate.setStyleSheet(f"background-color: {Styles.GREEN}; color: #000;")
        self.btn_calculate.clicked.connect(self.on_sell_click)
        
        self.result_label = QLabel("Sell Price: -")
        self.result_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {Styles.GREEN}; padding: 20px; background: #000; border-radius: 8px;")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        frame.layout.addWidget(QLabel("Cargo Details:"))
        frame.layout.addWidget(self.cargo_input)
        frame.layout.addWidget(QLabel("Destination UWP:"))
        frame.layout.addWidget(self.uwp_input)
        frame.layout.addLayout(broker_layout)
        frame.layout.addLayout(trade_layout)
        frame.layout.addWidget(self.btn_calculate)
        frame.layout.addWidget(self.result_label)
        
        layout.addWidget(frame)
        layout.addStretch()

    def on_sell_click(self):
        cargo = self.cargo_input.text()
        uwp = self.uwp_input.text().upper()
        
        if not cargo:
            self.result_label.setText("Error: No Cargo Code.")
            return
        if not self.uwp_pat.match(uwp):
            self.result_label.setText("Error: Incorrect UWP.")
            return
            
        try:
            trd = int(self.trade_roll.currentText())
            broker = int(self.broker_skill.currentText())
            value = cm.sell_price(cargo, uwp, broker, trd)
            if value > 0:
                self.result_label.setText(f"Sell Price: Cr{value:,}")
            else:
                self.result_label.setText("No value found.")
        except Exception as ex:
            self.result_label.setText(f"Error: {str(ex)}")
