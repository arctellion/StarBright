"""
PyQt6 view for the Pre-Made Armour Picker.
Provides an interface for selecting from pre-made armour configurations.
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QScrollArea, QFrame, QGroupBox, QLineEdit
from PyQt6.QtCore import Qt
import travtools.armourmaker as am
import random
import travtools.names as name_gen
import travtools.qrebs as qrebs_gen
from views.qt_components import Styles, GlassFrame

class PremadeArmourQtView(QWidget):
    """
    Main widget for the Pre-made Armour view.
    Handles the selection of pre-made body and head armor.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.update_output_premade()

    def init_ui(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)

        # --- Left Column: Selection ---
        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setFrameShape(QFrame.Shape.NoFrame)
        left_scroll_content = QWidget()
        left_layout = QVBoxLayout(left_scroll_content)
        left_layout.setSpacing(20)

        # Pre-made Picker
        pre_group = QGroupBox("Pre-made Armour Picker")
        pre_layout = QVBoxLayout(pre_group)
        self.pre_body = QComboBox()
        self.pre_body.addItem("(None)", "")
        for k, v in am.TYPES.items():
            if v["category"] == "Body": self.pre_body.addItem(v["name"], k)
        self.pre_body.currentIndexChanged.connect(self.update_output_premade)
        
        self.pre_head = QComboBox()
        self.pre_head.addItem("(None)", "")
        for k, v in am.TYPES.items():
            if v["category"] == "Head": self.pre_head.addItem(v["name"], k)
        self.pre_head.currentIndexChanged.connect(self.update_output_premade)

        pre_layout.addWidget(QLabel("Body Armour:"))
        pre_layout.addWidget(self.pre_body)
        pre_layout.addWidget(QLabel("Head Protection:"))
        pre_layout.addWidget(self.pre_head)
        left_layout.addWidget(pre_group)

        left_layout.addStretch()
        left_scroll.setWidget(left_scroll_content)
        self.main_layout.addWidget(left_scroll, 1)

        # --- Right Column: Profile ---
        right_column = QVBoxLayout()
        profile_frame = GlassFrame("Armor Profile", color=Styles.GREEN)
        
        self.res_model = QLabel("Model")
        self.res_model.setStyleSheet(f"font-size: 18px; color: {Styles.GREY_TEXT}; font-style: italic; border: none;")
        self.res_instance_name = QLabel("")
        self.res_instance_name.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {Styles.CYAN}; border: none;")
        self.res_name = QLabel("Type")
        self.res_name.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {Styles.AMBER}; border: none;")
        
        name_btn_layout = QHBoxLayout()
        self.btn_gen_name = QPushButton("Gen Name")
        self.btn_gen_name.clicked.connect(self.on_gen_name)
        self.btn_gen_name.setStyleSheet(f"background-color: {Styles.PURPLE}; color: {Styles.BG_COLOR}; max-width: 80px; font-size: 11px;")
        name_btn_layout.addWidget(self.res_instance_name)
        name_btn_layout.addWidget(self.btn_gen_name)
        name_btn_layout.addStretch()
        
        stats_layout = QHBoxLayout()
        self.res_tl = QLabel("TL: -")
        self.res_cost = QLabel("Cost: -")
        self.res_mass = QLabel("Mass: -")
        stats_layout.addWidget(self.res_tl)
        stats_layout.addWidget(self.res_cost)
        stats_layout.addWidget(self.res_mass)
        
        self.res_pills = QHBoxLayout()
        self.res_pills.setSpacing(5)
        
        attr_layout = QHBoxLayout()
        self.res_str = QLabel("STR: -")
        self.res_dex = QLabel("DEX: -")
        self.res_end = QLabel("END: -")
        attr_layout.addWidget(self.res_str)
        attr_layout.addWidget(self.res_dex)
        attr_layout.addWidget(self.res_end)
        
        self.res_notes = QLabel("")
        self.res_notes.setWordWrap(True)
        self.res_notes.setStyleSheet(f"color: {Styles.WHITE_TEXT}; font-size: 13px; border: none;")

        profile_frame.layout.addWidget(self.res_model)
        profile_frame.layout.addWidget(self.res_name)
        profile_frame.layout.addLayout(name_btn_layout)
        profile_frame.layout.addLayout(stats_layout)
        profile_frame.layout.addLayout(self.res_pills)
        profile_frame.layout.addWidget(QLabel("<hr/>"))
        profile_frame.layout.addLayout(attr_layout)
        profile_frame.layout.addWidget(QLabel("<b>Notes & Features</b>"))
        profile_frame.layout.addWidget(self.res_notes)
        
        # QREBS Section
        qrebs_group = QGroupBox("Production Quality")
        qrebs_layout = QVBoxLayout(qrebs_group)
        seed_layout = QHBoxLayout()
        self.seed_input = QLineEdit()
        self.seed_input.setPlaceholderText("Seed")
        self.btn_random = QPushButton("Random")
        self.btn_random.clicked.connect(self.randomize_qrebs)
        seed_layout.addWidget(self.seed_input)
        seed_layout.addWidget(self.btn_random)
        
        self.qrebs_res_code = QLabel("")
        self.qrebs_res_code.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {Styles.CYAN}; border: none;")
        self.qrebs_res_text = QLabel("")
        self.qrebs_res_text.setStyleSheet(f"font-size: 13px; color: {Styles.GREY_TEXT}; border: none;")
        self.qrebs_res_text.setWordWrap(True)
        
        qrebs_layout.addLayout(seed_layout)
        qrebs_layout.addWidget(self.qrebs_res_code)
        qrebs_layout.addWidget(self.qrebs_res_text)
        
        profile_frame.layout.addWidget(qrebs_group)
        profile_frame.layout.addStretch()

        right_column.addWidget(profile_frame)
        self.main_layout.addLayout(right_column, 1)

    def update_output_premade(self):
        res = am.calculate_premade_armor(self.pre_body.currentData(), self.pre_head.currentData(), "")
        self.last_res = res
        self.render_result(res)

    def on_gen_name(self):
        name = name_gen.generate_armour_name()
        self.res_instance_name.setText(name)

    def randomize_qrebs(self):
        self.seed_input.setText(str(random.randint(0, 100000)))
        # No direct way to update output here since it's premade, 
        # but render_result handles seed input.
        self.update_output_premade()

    def render_result(self, res):
        if not res: return
        self.res_name.setText(res["long_name"])
        self.res_model.setText(res["model"])
        self.res_tl.setText(f"TL: {res['tl']}")
        self.res_cost.setText(f"Cost: Cr {int(res['cost']):,}")
        
        qrebs_display = res['qrebs']
        if self.seed_input.text():
            try:
                q_res = qrebs_gen.generate_qrebs(seed=int(self.seed_input.text()), modifiers={'b': res.get('qrebs_mod', 0)})
                self.qrebs_res_code.setText(f"Instance Code: {q_res['code']}")
                self.qrebs_res_text.setText(q_res['text'])
                qrebs_display = q_res['code']
            except: pass
        else:
            self.qrebs_res_code.setText("")
            self.qrebs_res_text.setText("")

        self.res_mass.setText(f"Mass: {int(res['mass'])} kg | QREBS: {qrebs_display}")
        
        # Pills
        while self.res_pills.count():
            item = self.res_pills.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        
        labels = {'ar':'Ar','ca':'Ca','fl':'Fl','ra':'Ra','so':'So','ps':'Ps','ins':'In','seal':'Se'}
        for k, v in res['stats'].items():
            if v > 0 or (k == 'ar' and v == 0):
                lbl = QLabel(f"{labels[k]}={v}")
                lbl.setStyleSheet(f"background-color: {Styles.BG_COLOR}; color: {Styles.WHITE_TEXT}; padding: 2px 6px; border: 1px solid {Styles.BORDER_COLOR}; border-radius: 4px; font-weight: bold;")
                self.res_pills.addWidget(lbl)
        self.res_pills.addStretch()

        ev = res['eval']
        self.res_str.setText(f"STR: x{ev['strMult']}" if ev['strMult'] != 1 else f"STR: {ev['str']}")
        self.res_dex.setText(f"DEX: {'+' if ev['dex']>0 else ''}{ev['dex']}")
        self.res_end.setText(f"END: {'+' if ev['end']>0 else ''}{ev['end']}")
        
        notes = []
        if res.get("standards"): notes.append(f"<font color='{Styles.GREEN}'>Standard: {', '.join(res['standards'])}</font>")
        if res.get("extras"): notes.append(f"<font color='{Styles.CYAN}'>Additional: {', '.join(res['extras'])}</font>")
        if res.get("drawbacks"): notes.append(f"<font color='{Styles.AMBER}'>Drawbacks: {', '.join(res['drawbacks'])}</font>")
        if res.get("notes"): notes.append(res['notes'])
        self.res_notes.setText("<br>".join(notes))
