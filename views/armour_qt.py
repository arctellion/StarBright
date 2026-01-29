from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QCheckBox, QScrollArea, QFrame, QGridLayout, QGroupBox, QLineEdit
from PyQt6.QtCore import Qt
import travtools.armourmaker as am
import random
from views.qt_components import Styles, GlassFrame

class ArmourQtView(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_opts = set(am.STANDARD_SUBSYSTEMS.get("D", []))
        self.selected_drawbacks = {}
        self.last_type = "D"
        self.sub_cbs = {}
        self.sub_drawbacks = {}
        self.init_ui()
        self.update_output()

    def init_ui(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)

        # --- Left Column: Design & Subsystems ---
        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setFrameShape(QFrame.Shape.NoFrame)
        left_scroll_content = QWidget()
        left_layout = QVBoxLayout(left_scroll_content)
        left_layout.setSpacing(20)

        # Custom Design Frame
        custom_group = QGroupBox("Custom Armour Design")
        custom_layout = QVBoxLayout(custom_group)
        
        self.type_combo = QComboBox()
        for k, v in am.TYPES.items():
            if v['type'] == 'System':
                self.type_combo.addItem(f"{v['name']} (TL{v['tl']})", k)
        self.type_combo.setCurrentIndex(self.type_combo.findData("D"))
        self.type_combo.currentIndexChanged.connect(self.on_type_change)
        
        self.desc_combo = QComboBox()
        for k in am.MODIFIERS["descriptor"].keys():
            self.desc_combo.addItem(k or "(Blank)", k)
        self.desc_combo.currentIndexChanged.connect(self.update_output)
        
        self.burden_combo = QComboBox()
        for k in am.MODIFIERS["burden"].keys():
            self.burden_combo.addItem(k or "(Blank)", k)
        self.burden_combo.currentIndexChanged.connect(self.update_output)
        
        self.stage_combo = QComboBox()
        for k in am.MODIFIERS["stage"].keys():
            self.stage_combo.addItem(k or "(Blank)", k)
        self.stage_combo.currentIndexChanged.connect(self.update_output)
        
        self.user_combo = QComboBox()
        for k, v in am.USERS.items():
            self.user_combo.addItem(v['name'], k)
        self.user_combo.currentIndexChanged.connect(self.update_output)

        custom_layout.addWidget(QLabel("Armor Type:"))
        custom_layout.addWidget(self.type_combo)
        custom_layout.addWidget(QLabel("Descriptor:"))
        custom_layout.addWidget(self.desc_combo)
        custom_layout.addWidget(QLabel("Burden:"))
        custom_layout.addWidget(self.burden_combo)
        custom_layout.addWidget(QLabel("Stage:"))
        custom_layout.addWidget(self.stage_combo)
        custom_layout.addWidget(QLabel("User:"))
        custom_layout.addWidget(self.user_combo)
        left_layout.addWidget(custom_group)

        # Subsystems
        sub_group = QGroupBox("Subsystems")
        sub_layout = QVBoxLayout(sub_group)
        for cat, ids in am.SUBSYSTEM_CATS.items():
            cat_group = QGroupBox(cat.capitalize())
            cat_layout = QVBoxLayout(cat_group)
            for opt_id in ids:
                v = next((o for o in am.OPTIONS if o["id"] == opt_id), None)
                if not v: continue
                
                cb_layout = QVBoxLayout()
                cb = QCheckBox(v['name'])
                cb.setProperty("opt_id", opt_id)
                cb.stateChanged.connect(self.on_cb_change)
                self.sub_cbs[opt_id] = cb
                
                db_lbl = QLabel("")
                db_lbl.setStyleSheet(f"color: {Styles.AMBER}; font-size: 11px; font-style: italic; margin-left: 20px;")
                db_lbl.setVisible(False)
                self.sub_drawbacks[opt_id] = db_lbl
                
                cb_layout.addWidget(cb)
                cb_layout.addWidget(db_lbl)
                cat_layout.addLayout(cb_layout)
            sub_layout.addWidget(cat_group)
        left_layout.addWidget(sub_group)

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
        self.res_name = QLabel("Name")
        self.res_name.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {Styles.AMBER}; border: none;")
        
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
        profile_frame.layout.addLayout(stats_layout)
        profile_frame.layout.addLayout(self.res_pills)
        profile_frame.layout.addWidget(QLabel("<hr/>"))
        profile_frame.layout.addLayout(attr_layout)
        profile_frame.layout.addWidget(QLabel("<b>Notes & Features</b>"))
        profile_frame.layout.addWidget(self.res_notes)
        profile_frame.layout.addStretch()

        right_column.addWidget(profile_frame)
        self.main_layout.addLayout(right_column, 1)

    def on_cb_change(self, state):
        cb = self.sender()
        opt_id = cb.property("opt_id")
        if state == Qt.CheckState.Checked.value:
            self.selected_opts.add(opt_id)
            standards = am.STANDARD_SUBSYSTEMS.get(self.type_combo.currentData(), [])
            if opt_id not in standards:
                extras = [o for o in self.selected_opts if o not in standards]
                table_num = 1 if len(extras) == 1 else (2 + (len(extras)-2)%3)
                self.selected_drawbacks[opt_id] = random.choice(am.DRAWBACKS[table_num])["id"]
        else:
            self.selected_opts.discard(opt_id)
            self.selected_drawbacks.pop(opt_id, None)
        self.update_output()
        self.refresh_cb_styles()

    def on_type_change(self):
        new_type = self.type_combo.currentData()
        old_standards = set(am.STANDARD_SUBSYSTEMS.get(self.last_type, []))
        new_standards = set(am.STANDARD_SUBSYSTEMS.get(new_type, []))
        self.selected_opts = {opt for opt in self.selected_opts if opt not in old_standards}
        self.selected_opts.update(new_standards)
        for opt_id in list(self.selected_drawbacks.keys()):
            if opt_id in new_standards: del self.selected_drawbacks[opt_id]
        self.last_type = new_type
        self.update_output()
        self.refresh_cb_styles()

    def refresh_cb_styles(self):
        standards = am.STANDARD_SUBSYSTEMS.get(self.type_combo.currentData(), [])
        for opt_id, cb in self.sub_cbs.items():
            v = next((o for o in am.OPTIONS if o["id"] == opt_id), None)
            is_std = opt_id in standards
            is_sel = opt_id in self.selected_opts
            cb.blockSignals(True)
            cb.setChecked(is_sel)
            cb.blockSignals(False)
            cb.setText(f"{v['name']} (Standard)" if is_std else v['name'])
            cb.setStyleSheet(f"color: {Styles.GREEN if is_std else Styles.WHITE_TEXT}")
            
            db_lbl = self.sub_drawbacks[opt_id]
            if is_sel and not is_std and opt_id in self.selected_drawbacks:
                db_id = self.selected_drawbacks[opt_id]
                db_name = next((d['name'] for p in am.DRAWBACKS.values() for d in p if d['id'] == db_id), "Unknown")
                db_lbl.setText(f"↳ Drawback: {db_name}")
                db_lbl.setVisible(True)
            else:
                db_lbl.setVisible(False)

    def update_output(self):
        res = am.calculate_custom_armor(self.type_combo.currentData(), self.desc_combo.currentData(), self.burden_combo.currentData(), self.stage_combo.currentData(), self.user_combo.currentData(), list(self.selected_opts), self.selected_drawbacks)
        self.render_result(res)

    def update_output_premade(self):
        res = am.calculate_premade_armor(self.pre_body.currentData(), self.pre_head.currentData(), "")
        self.render_result(res)

    def render_result(self, res):
        if not res: return
        self.res_name.setText(res["long_name"])
        self.res_model.setText(res["model"])
        self.res_tl.setText(f"TL: {res['tl']}")
        self.res_cost.setText(f"Cost: Cr {int(res['cost']):,}")
        self.res_mass.setText(f"Mass: {int(res['mass'])} kg")
        
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
