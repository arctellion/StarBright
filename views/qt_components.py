from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

class Styles:
    BG_COLOR = "#0B0E14"
    CARD_BG = "#161B22"
    BORDER_COLOR = "#30363D"
    
    # Accent Colors
    AMBER = "#FFC107"
    BLUE = "#42A5F5"
    GREEN = "#66BB6A"
    CYAN = "#26C6DA"
    PURPLE = "#AB47BC"
    TEAL = "#26A69A"
    GREY_TEXT = "#8B949E"
    WHITE_TEXT = "#C9D1D9"

    MAIN_STYLE = f"""
        QMainWindow, QWidget {{
            background-color: {BG_COLOR};
            color: {WHITE_TEXT};
            font-family: 'Segoe UI', sans-serif;
        }}
        QMenuBar {{
            background-color: {CARD_BG};
            border-bottom: 1px solid {BORDER_COLOR};
        }}
        QMenuBar::item {{
            padding: 8px 12px;
            background: transparent;
        }}
        QMenuBar::item:selected {{
            background-color: {BLUE};
            color: {BG_COLOR};
        }}
        QMenu {{
            background-color: {CARD_BG};
            border: 1px solid {BORDER_COLOR};
        }}
        QMenu::item {{
            padding: 8px 24px;
        }}
        QMenu::item:selected {{
            background-color: {BLUE};
            color: {BG_COLOR};
        }}
        QMenu::item:disabled {{
            color: {GREY_TEXT};
        }}
        QLineEdit {{
            background-color: {BG_COLOR};
            border: 1px solid {BORDER_COLOR};
            border-radius: 4px;
            padding: 5px;
            color: {WHITE_TEXT};
        }}
        QLineEdit:focus {{
            border: 1px solid {BLUE};
        }}
        QPushButton {{
            background-color: {BLUE};
            color: {BG_COLOR};
            border-radius: 4px;
            padding: 8px 15px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: #64B5F6;
        }}
        QPushButton:pressed {{
            background-color: #2196F3;
        }}
        QGroupBox {{
            border: 1px solid {BORDER_COLOR};
            border-radius: 8px;
            margin-top: 15px;
            padding-top: 10px;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px 0 3px;
        }}
        QScrollBar:vertical {{
            border: none;
            background: {BG_COLOR};
            width: 10px;
            margin: 0px;
        }}
        QScrollBar::handle:vertical {{
            background: {BORDER_COLOR};
            min-height: 20px;
            border-radius: 5px;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
    """

class GlassFrame(QFrame):
    def __init__(self, title=None, subtitle=None, color=Styles.BLUE):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Styles.CARD_BG};
                border: 1px solid {Styles.BORDER_COLOR};
                border-radius: 12px;
            }}
        """)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)
        
        if title:
            self.title_label = QLabel(title)
            self.title_label.setStyleSheet(f"color: {color}; font-size: 20px; font-weight: bold; border: none; background: transparent;")
            self.layout.addWidget(self.title_label)
        
        if subtitle:
            self.sub_label = QLabel(subtitle)
            self.sub_label.setStyleSheet(f"color: {Styles.GREY_TEXT}; font-size: 13px; border: none; background: transparent;")
            self.layout.addWidget(self.sub_label)

    def addWidget(self, widget):
        self.layout.addWidget(widget)

class NumericSpinner(QHBoxLayout):
    def __init__(self, label, value=0, min_val=0, max_val=99):
        super().__init__()
        self.min_val = min_val
        self.max_val = max_val
        
        self.lbl = QLabel(label)
        self.lbl.setStyleSheet("border: none; background: transparent;")
        
        self.btn_minus = QPushButton("-")
        self.btn_minus.setFixedWidth(30)
        self.btn_minus.clicked.connect(self.decrement)
        
        self.edit = QLineEdit(str(value))
        self.edit.setFixedWidth(60)
        self.edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.btn_plus = QPushButton("+")
        self.btn_plus.setFixedWidth(30)
        self.btn_plus.clicked.connect(self.increment)
        
        self.addWidget(self.lbl)
        self.addStretch()
        self.addWidget(self.btn_minus)
        self.addWidget(self.edit)
        self.addWidget(self.btn_plus)

    def increment(self):
        try:
            val = int(self.edit.text())
            if val < self.max_val:
                self.edit.setText(str(val + 1))
        except:
            self.edit.setText(str(self.min_val))

    def decrement(self):
        try:
            val = int(self.edit.text())
            if val > self.min_val:
                self.edit.setText(str(val - 1))
        except:
            self.edit.setText(str(self.min_val))

    @property
    def value(self):
        try:
            return int(self.edit.text())
        except:
            return self.min_val
