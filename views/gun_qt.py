"""
PyQt6 view for the Gun Maker utility.
Provides an interface for designing custom weapons, calculating their 
statistics, and generating QREBS quality assessments.
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QCheckBox, QScrollArea, QFrame, QGridLayout, QGroupBox, QLineEdit
from PyQt6.QtCore import Qt
import travtools.gunmaker as gm
import travtools.qrebs as qrebs_gen
import travtools.names as name_gen
import random
from views.qt_components import Styles, GlassFrame

class GunQtView(QWidget):
    """
    Main widget for the Gun Maker view.
    Handles weapon core selection, modifications, and result visualization.
    """
    def __init__(self):
        super().__init__()
        self.burden_cbs = {}
        self.stage_cbs = {}
        self.option_cbs = {}
        self.is_generated = False
        self.init_ui()
        self.update_gm_desc()

    def init_ui(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)

        # --- Left Column: Controls ---
        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setFrameShape(QFrame.Shape.NoFrame)
        left_scroll_content = QWidget()
        left_layout = QVBoxLayout(left_scroll_content)
        left_layout.setSpacing(20)

        # Weapon Core
        core_frame = GlassFrame("Weapon Core", color=Styles.AMBER)
        self.type_combo = QComboBox()
        for cat, types in gm.CHART_3_TYPES.items():
            for code, data in types.items():
                self.type_combo.addItem(f"{cat}: {data['name']} (TL{data['tl']})", f"{cat}|{code}")
        self.type_combo.currentIndexChanged.connect(self.update_gm_desc)
        
        self.desc_combo = QComboBox()
        self.desc_combo.currentIndexChanged.connect(self.update_gm_output)
        
        self.user_combo = QComboBox()
        for k, v in gm.CHART_5_USER.items():
            self.user_combo.addItem(v['name'], k)
        self.user_combo.setCurrentText("Medium (Human)")
        self.user_combo.currentIndexChanged.connect(self.update_gm_output)
        
        self.port_combo = QComboBox()
        self.port_combo.addItems(["Auto-Calculate", "Personal", "Crewed", "Fixed", "Portable", "Vehicle", "Turret"])
        self.port_combo.currentIndexChanged.connect(self.update_gm_output)

        core_frame.layout.addWidget(QLabel("Category & Type:"))
        core_frame.layout.addWidget(self.type_combo)
        core_frame.layout.addWidget(QLabel("Descriptor:"))
        core_frame.layout.addWidget(self.desc_combo)
        core_frame.layout.addWidget(QLabel("User:"))
        core_frame.layout.addWidget(self.user_combo)
        core_frame.layout.addWidget(QLabel("Portability:"))
        core_frame.layout.addWidget(self.port_combo)
        left_layout.addWidget(core_frame)

        # Modifications
        mod_frame = GlassFrame("Modifications", color=Styles.CYAN)
        
        # Burden
        burden_group = QGroupBox("Burden")
        burden_layout = QVBoxLayout(burden_group)
        for k, v in gm.CHART_5_BURDEN.items():
            cb = QCheckBox(v['name'])
            cb.stateChanged.connect(self.update_gm_output)
            self.burden_cbs[k] = cb
            burden_layout.addWidget(cb)
        mod_frame.layout.addWidget(burden_group)
        
        # Stage
        stage_group = QGroupBox("Stage")
        stage_layout = QVBoxLayout(stage_group)
        for k, v in gm.CHART_5_STAGE.items():
            cb = QCheckBox(v['name'])
            cb.stateChanged.connect(self.update_gm_output)
            self.stage_cbs[k] = cb
            stage_layout.addWidget(cb)
        mod_frame.layout.addWidget(stage_group)
        
        # Options
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout(options_group)
        for k, v in gm.CHART_7_OPTIONS.items():
            cb = QCheckBox(v)
            cb.stateChanged.connect(self.update_gm_output)
            self.option_cbs[k] = cb
            options_layout.addWidget(cb)
        mod_frame.layout.addWidget(options_group)
        
        left_layout.addWidget(mod_frame)
        left_layout.addStretch()
        left_scroll.setWidget(left_scroll_content)
        self.main_layout.addWidget(left_scroll, 1)

        # --- Right Column: Profile ---
        right_column = QVBoxLayout()
        profile_frame = GlassFrame("Weapon Profile", color=Styles.GREEN)
        
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
        
        self.res_stats = QLabel("")
        self.res_stats.setStyleSheet("font-size: 16px; border: none;")
        
        self.res_effects = QLabel("")
        self.res_effects.setStyleSheet(f"font-size: 14px; color: {Styles.WHITE_TEXT}; border: none;")
        
        self.res_controls = QHBoxLayout()
        
        self.res_wx = QLabel("Wx: ...")
        self.res_wx.setStyleSheet(f"background-color: #000; color: {Styles.CYAN}; padding: 10px; border-radius: 5px; font-family: monospace; border: 1px solid {Styles.BORDER_COLOR};")
        self.res_wx.setWordWrap(True)
        self.res_wx.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

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

        profile_frame.layout.addWidget(self.res_model)
        profile_frame.layout.addWidget(self.res_name)
        profile_frame.layout.addLayout(name_btn_layout)
        profile_frame.layout.addWidget(QLabel("<hr/>"))
        profile_frame.layout.addWidget(self.res_stats)
        profile_frame.layout.addWidget(QLabel("<b>Effects</b>"))
        profile_frame.layout.addWidget(self.res_effects)
        profile_frame.layout.addWidget(QLabel("<b>Controls</b>"))
        profile_frame.layout.addLayout(self.res_controls)
        profile_frame.layout.addWidget(self.res_wx)
        profile_frame.layout.addWidget(qrebs_group)
        profile_frame.layout.addStretch()

        right_column.addWidget(profile_frame)
        self.main_layout.addLayout(right_column, 1)

    def update_gm_desc(self):
        data = self.type_combo.currentData()
        if not data: return
        cat, code = data.split("|")
        self.desc_combo.clear()
        for k, v in gm.CHART_4_DESCRIPTORS[cat].items():
            self.desc_combo.addItem(v['name'] or "(None)", k)
        self.update_gm_output()

    def randomize_qrebs(self):
        self.seed_input.setText(str(random.randint(0, 100000)))
        self.is_generated = True
        self.update_gm_output()

    def on_gen_name(self):
        name = name_gen.generate_gun_name()
        self.res_instance_name.setText(name)

    def update_gm_output(self):
        data = self.type_combo.currentData()
        if not data: return
        cat, t_code = data.split("|")
        d_code = self.desc_combo.currentData()
        b_codes = [k for k, cb in self.burden_cbs.items() if cb.isChecked()]
        s_codes = [k for k, cb in self.stage_cbs.items() if cb.isChecked()]
        o_codes = [k for k, cb in self.option_cbs.items() if cb.isChecked()]
        user = self.user_combo.currentData()
        port = self.port_combo.currentText()
        if port == "Auto-Calculate": port = "auto"

        try:
            res = gm.calculate_weapon(cat, t_code, d_code, b_codes, s_codes, user, port, o_codes)
            
            # QREBS Generation
            qrebs_display = res['qrebs']
            if self.is_generated:
                try:
                    q_res = qrebs_gen.generate_qrebs(seed=int(self.seed_input.text()), modifiers={'b': res.get('qrebs_mod', 0)})
                    self.qrebs_res_code.setText(f"Instance Code: {q_res['code']}")
                    self.qrebs_res_text.setText(q_res['text'])
                    qrebs_display = q_res['code']
                except: pass
            else:
                self.qrebs_res_code.setText("")
                self.qrebs_res_text.setText("")

            self.res_model.setText(res['model'])
            self.res_name.setText(res['long_name'])
            
            stats_text = f"TL: {res['tl']} | Range: {res['range']} | Mass: {res['mass']:.2f} kg | Cost: Cr {int(res['cost']):,}"
            if self.is_generated: stats_text += f" | QREBS: {qrebs_display}"
            self.res_stats.setText(stats_text)
            
            effects_text = "\n".join([f"• {k}: {v}" for k, v in res['effects'].items()])
            self.res_effects.setText(effects_text)
            
            # Clear and rebuild controls
            while self.res_controls.count():
                item = self.res_controls.takeAt(0)
                if item.widget(): item.widget().deleteLater()
            
            ctrl_labels = {"off": "Safe", "single": "Semi", "burst": "Burst", "full": "Auto", "p123": "1-2-3", "override": "Ovrd"}
            for k, v in res['controls'].items():
                if v:
                    lbl = QLabel(ctrl_labels[k])
                    lbl.setStyleSheet(f"padding: 3px 8px; border: 1px solid {Styles.AMBER}; border-radius: 4px; color: {Styles.AMBER}; font-size: 11px;")
                    self.res_controls.addWidget(lbl)
            self.res_controls.addStretch()

            eff_str = " ".join([f"{k}-{v}" for k, v in res['effects'].items()])
            self.res_wx.setText(f"Wx: R={res['range']} Cr{int(res['cost']):,} {res['mass']:.1f}kg B={res['base_qrebs']} {eff_str}")
        except Exception as e:
            print(f"GunMaker Error: {e}")
