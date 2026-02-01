from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, QGroupBox
from PyQt6.QtCore import Qt
import travtools.names as names
from views.qt_components import Styles, GlassFrame

class NamesQtView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        main_frame = GlassFrame("Random Name Generator", "Generate names for characters, planets, and objects", Styles.PURPLE)
        
        # Generator Controls
        controls_group = QGroupBox("Configuration")
        controls_layout = QVBoxLayout(controls_group)
        
        # Type Selection
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Generator Type:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Character", "Planet", "Object"])
        self.type_combo.currentTextChanged.connect(self.on_type_changed)
        type_layout.addWidget(self.type_combo)
        controls_layout.addLayout(type_layout)
        
        # Gender Selection (only for character)
        self.gender_layout = QHBoxLayout()
        self.gender_label = QLabel("Gender:")
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female", "Neutral"])
        self.gender_layout.addWidget(self.gender_label)
        self.gender_layout.addWidget(self.gender_combo)
        controls_layout.addLayout(self.gender_layout)
        
        # Planet Specific inputs (Hex & UWP) - hidden by default
        self.planet_inputs = QWidget()
        planet_layout = QVBoxLayout(self.planet_inputs)
        
        hex_layout = QHBoxLayout()
        hex_layout.addWidget(QLabel("Hex Location:"))
        self.hex_input = QLineEdit("0101")
        hex_layout.addWidget(self.hex_input)
        planet_layout.addLayout(hex_layout)
        
        uwp_layout = QHBoxLayout()
        uwp_layout.addWidget(QLabel("UWP:"))
        self.uwp_input = QLineEdit("E56789A-B")
        uwp_layout.addWidget(self.uwp_input)
        planet_layout.addLayout(uwp_layout)
        
        controls_layout.addWidget(self.planet_inputs)
        self.planet_inputs.hide()
        
        # Generate Button
        self.btn_generate = QPushButton("Generate Name")
        self.btn_generate.setStyleSheet(f"background-color: {Styles.PURPLE}; color: {Styles.BG_COLOR};")
        self.btn_generate.clicked.connect(self.on_generate)
        controls_layout.addWidget(self.btn_generate)
        
        main_frame.layout.addWidget(controls_group)
        
        # Result Display
        result_group = QGroupBox("Result")
        result_layout = QVBoxLayout(result_group)
        
        self.result_display = QLineEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {Styles.WHITE_TEXT}; height: 50px;")
        result_layout.addWidget(self.result_display)
        
        btn_copy = QPushButton("Copy to Clipboard")
        btn_copy.clicked.connect(self.on_copy)
        result_layout.addWidget(btn_copy)
        
        main_frame.layout.addWidget(result_group)
        
        layout.addWidget(main_frame)
        layout.addStretch()

    def on_type_changed(self, text):
        if text == "Character":
            self.gender_label.show()
            self.gender_combo.show()
            self.planet_inputs.hide()
        elif text == "Planet":
            self.gender_label.hide()
            self.gender_combo.hide()
            self.planet_inputs.show()
        else:
            self.gender_label.hide()
            self.gender_combo.hide()
            self.planet_inputs.hide()

    def on_generate(self):
        gen_type = self.type_combo.currentText()
        if gen_type == "Character":
            gender = self.gender_combo.currentText()
            name = names.generate_character_name(gender)
        elif gen_type == "Planet":
            loc = self.hex_input.text()
            uwp = self.uwp_input.text()
            try:
                name = names.generate_planet_name(loc, uwp)
            except Exception as e:
                name = f"Error: {str(e)}"
        else:
            name = names.generate_object_name()
            
        self.result_display.setText(name)

    def on_copy(self):
        from PyQt6.QtWidgets import QApplication
        QApplication.clipboard().setText(self.result_display.text())
