from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget, QScrollArea, QFrame, QGridLayout
from PyQt6.QtCore import Qt
import travtools.dice as dd
from views.qt_components import Styles, GlassFrame

class DiceQtView(QWidget):
    def __init__(self):
        super().__init__()
        self.history = []
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)

        # 1. Controls Section
        controls_frame = GlassFrame("Dice Roller", "Quick options and custom rolls", Styles.AMBER)
        
        # Quick Roll Buttons Grid
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        
        quick_rolls = [
            ("Easy (1d6)", 1),
            ("Average (2d6)", 2),
            ("Difficult (3d6)", 3),
            ("Formidable (4d6)", 4),
            ("Staggering (5d6)", 5),
            ("Impossible (6d6)", 6),
        ]
        
        for i, (label, n) in enumerate(quick_rolls):
            btn = QPushButton(label)
            btn.setMinimumHeight(40)
            btn.clicked.connect(lambda checked, n=n: self.roll_dice(n))
            grid_layout.addWidget(btn, i // 3, i % 3)
            
        # Flux Button
        flux_btn = QPushButton("Flux (2d6-7)")
        flux_btn.setMinimumHeight(40)
        flux_btn.clicked.connect(self.roll_flux)
        grid_layout.addWidget(flux_btn, 2, 0, 1, 3) # Span across 3 columns
        
        controls_frame.layout.addLayout(grid_layout)
        
        # Custom Roll Input
        custom_layout = QHBoxLayout()
        self.custom_input = QLineEdit("2d6")
        self.custom_input.setPlaceholderText("e.g., 2d6+3")
        self.custom_input.returnPressed.connect(self.on_custom_roll)
        
        roll_btn = QPushButton("Roll Custom")
        roll_btn.clicked.connect(self.on_custom_roll)
        
        custom_layout.addWidget(self.custom_input)
        custom_layout.addWidget(roll_btn)
        controls_frame.layout.addLayout(custom_layout)
        
        self.main_layout.addWidget(controls_frame)

        # 2. Results and History Section
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)
        
        # Result Display
        self.result_frame = GlassFrame("Result")
        self.result_frame.setMinimumHeight(200)
        self.result_text = QLabel("Dice Roll")
        self.result_text.setStyleSheet(f"font-size: 48px; font-weight: 900; color: {Styles.AMBER}; border: none; background: transparent;")
        self.result_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.detail_text = QLabel("")
        self.detail_text.setStyleSheet(f"font-size: 16px; color: {Styles.GREY_TEXT}; border: none; background: transparent;")
        self.detail_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.result_frame.layout.addWidget(self.result_text)
        self.result_frame.layout.addWidget(self.detail_text)
        self.result_frame.layout.addStretch()
        
        # History
        self.history_frame = GlassFrame("History")
        self.history_frame.setMinimumHeight(200)
        self.history_list = QListWidget()
        self.history_list.setStyleSheet(f"border: none; background: transparent; color: {Styles.WHITE_TEXT}; font-size: 14px;")
        self.history_frame.layout.addWidget(self.history_list)
        
        bottom_layout.addWidget(self.result_frame, 3)
        bottom_layout.addWidget(self.history_frame, 2)
        
        self.main_layout.addLayout(bottom_layout)
        self.main_layout.addStretch()

    def roll_dice(self, n):
        total, rolls = dd.dice_detailed(n)
        self.update_display(f"{n}d6", total, rolls)

    def roll_flux(self):
        # Flux (2d6-7)
        total = dd.dice(2) - 7
        self.update_display("Flux (2d6-7)", total, "2d6-7")

    def on_custom_roll(self):
        try:
            total, rolls, mod = dd.roll_string(self.custom_input.text())
            details = f"{rolls} + {mod}" if mod else f"{rolls}"
            self.update_display(self.custom_input.text(), total, details)
        except Exception as ex:
            self.result_text.setText("Error")
            self.detail_text.setText(str(ex))

    def update_display(self, label, total, details):
        self.result_text.setText(str(total))
        self.detail_text.setText(f"Rolled {label}: {details}")
        
        # Add to history
        item_text = f"{label}: {total} ({details})"
        self.history_list.insertItem(0, item_text)
        
        # Keep history reasonable
        if self.history_list.count() > 20:
            self.history_list.takeItem(self.history_list.count() - 1)
