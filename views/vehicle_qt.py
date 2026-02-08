"""
PyQt6 view for the Vehicle Maker utility.
Provides an interface for designing Ground, Flyer, Water, and Military vehicles.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QComboBox, QScrollArea, QFrame, QGroupBox, QTabWidget, QGridLayout)
from PyQt6.QtCore import Qt
import travtools.vehiclemaker as vm
from views.qt_components import Styles, GlassFrame

class VehicleQtView(QWidget):
    """
    Main widget for the Vehicle Maker view.
    Includes tabs for different vehicle categories.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.update_all_outputs()

    def init_ui(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)

        # --- Left Column: Tabs for Categories ---
        self.tabs = QTabWidget()
        
        # We'll create a tab for each category
        self.ground_tab = self.create_category_tab("ground", vm.GROUND, vm.GR_MISSION, vm.GR_MOTIVE)
        self.flyer_tab = self.create_category_tab("flyer", vm.FLYERS, vm.F_MISSION, vm.F_MOTIVE)
        self.water_tab = self.create_category_tab("watercraft", vm.WATERCRAFT, vm.W_MISSION, vm.W_MOTIVE)
        self.military_tab = self.create_category_tab("military", vm.MILITARY, vm.M_MISSION, vm.M_MOTIVE)
        
        self.tabs.addTab(self.ground_tab, "Ground")
        self.tabs.addTab(self.flyer_tab, "Flyers")
        self.tabs.addTab(self.water_tab, "Watercraft")
        self.tabs.addTab(self.military_tab, "Military")
        
        self.tabs.currentChanged.connect(self.update_all_outputs)
        
        self.main_layout.addWidget(self.tabs, 1)

        # --- Right Column: Profile ---
        right_column = QVBoxLayout()
        self.profile_frame = GlassFrame("Vehicle Profile", color=Styles.CYAN)
        
        self.res_type = QLabel("Type")
        self.res_type.setStyleSheet(f"font-size: 18px; color: {Styles.GREY_TEXT}; font-style: italic; border: none;")
        self.res_name = QLabel("Name")
        self.res_name.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {Styles.AMBER}; border: none;")
        
        stats_layout = QHBoxLayout()
        self.res_tl = QLabel("TL: -")
        self.res_cost = QLabel("Cost: -")
        self.res_mass = QLabel("Vol/Mass: -")
        stats_layout.addWidget(self.res_tl)
        stats_layout.addWidget(self.res_cost)
        stats_layout.addWidget(self.res_mass)
        
        self.res_pills = QGridLayout()
        self.res_pills.setSpacing(5)
        
        self.res_speed = QLabel("Speed: -")
        self.res_load = QLabel("Load: -")
        self.res_q = QLabel("Q: -")
        
        perf_layout = QHBoxLayout()
        perf_layout.addWidget(self.res_speed)
        perf_layout.addWidget(self.res_load)
        perf_layout.addWidget(self.res_q)

        self.profile_frame.layout.addWidget(self.res_type)
        self.profile_frame.layout.addWidget(self.res_name)
        self.profile_frame.layout.addLayout(stats_layout)
        self.profile_frame.layout.addWidget(QLabel("<hr/>"))
        self.profile_frame.layout.addLayout(perf_layout)
        self.profile_frame.layout.addWidget(QLabel("<b>Armor Values</b>"))
        self.profile_frame.layout.addLayout(self.res_pills)
        self.profile_frame.layout.addStretch()

        right_column.addWidget(self.profile_frame)
        self.main_layout.addLayout(right_column, 1)

    def create_category_tab(self, category, bases, missions, motives):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        content = QWidget()
        scroll_layout = QVBoxLayout(content)
        
        group = QGroupBox(f"{category.capitalize()} Configuration")
        form_layout = QVBoxLayout(group)
        
        combos = {}
        
        # Base Craft
        base_combo = QComboBox()
        for i, b in enumerate(bases):
            base_combo.addItem(b[1], i)
        base_combo.currentIndexChanged.connect(self.update_all_outputs)
        combos['base'] = base_combo
        form_layout.addWidget(QLabel("Base Craft:"))
        form_layout.addWidget(base_combo)
        
        # Mission
        mission_combo = QComboBox()
        for i, m in enumerate(missions):
            mission_combo.addItem(m[1], i)
        mission_combo.currentIndexChanged.connect(self.update_all_outputs)
        combos['mission'] = mission_combo
        form_layout.addWidget(QLabel("Mission:"))
        form_layout.addWidget(mission_combo)
        
        # Motive
        motive_combo = QComboBox()
        for i, m in enumerate(motives):
            motive_combo.addItem(m[1], i)
        motive_combo.currentIndexChanged.connect(self.update_all_outputs)
        combos['motive'] = motive_combo
        form_layout.addWidget(QLabel("Motive System:"))
        form_layout.addWidget(motive_combo)
        
        # Bulk
        bulk_combo = QComboBox()
        for i, b in enumerate(vm.BULK):
            bulk_combo.addItem(b[1], i)
        bulk_combo.currentIndexChanged.connect(self.update_all_outputs)
        combos['bulk'] = bulk_combo
        form_layout.addWidget(QLabel("Bulk/Size:"))
        form_layout.addWidget(bulk_combo)
        
        # Stage
        stage_combo = QComboBox()
        for i, s in enumerate(vm.STAGE):
            stage_combo.addItem(s[1], i)
        stage_combo.currentIndexChanged.connect(self.update_all_outputs)
        combos['stage'] = stage_combo
        form_layout.addWidget(QLabel("Stage:"))
        form_layout.addWidget(stage_combo)
        
        # Descriptor
        desc_combo = QComboBox()
        for i, d in enumerate(vm.DESCRIPTORS):
            desc_combo.addItem(d[1], i)
        desc_combo.currentIndexChanged.connect(self.update_all_outputs)
        combos['desc'] = desc_combo
        form_layout.addWidget(QLabel("Descriptor:"))
        form_layout.addWidget(desc_combo)
        
        # Options (Simplified as two dropdowns)
        opt1_combo = QComboBox()
        opt1_combo.addItem("(None)", 0)
        for i, o in enumerate(vm.OPT[1:], 1):
             opt1_combo.addItem(o[1], i)
        opt1_combo.currentIndexChanged.connect(self.update_all_outputs)
        combos['opt1'] = opt1_combo
        form_layout.addWidget(QLabel("Option 1:"))
        form_layout.addWidget(opt1_combo)

        opt2_combo = QComboBox()
        opt2_combo.addItem("(None)", 0)
        for i, o in enumerate(vm.OPT[1:], 1):
             opt2_combo.addItem(o[1], i)
        opt2_combo.currentIndexChanged.connect(self.update_all_outputs)
        combos['opt2'] = opt2_combo
        form_layout.addWidget(QLabel("Option 2:"))
        form_layout.addWidget(opt2_combo)
        
        # Endurance
        end_combo = QComboBox()
        for i, e in enumerate(vm.ENDURANCE):
            end_combo.addItem(e[1], i)
        end_combo.currentIndexChanged.connect(self.update_all_outputs)
        combos['end'] = end_combo
        form_layout.addWidget(QLabel("Endurance:"))
        form_layout.addWidget(end_combo)
        
        scroll_layout.addWidget(group)
        scroll_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        tab.combos = combos
        tab.category = category
        return tab

    def update_all_outputs(self):
        current_tab = self.tabs.currentWidget()
        if not current_tab: return
        
        c = current_tab.combos
        opt_idxs = []
        if c['opt1'].currentData() > 0: opt_idxs.append(c['opt1'].currentData())
        if c['opt2'].currentData() > 0: opt_idxs.append(c['opt2'].currentData())
        
        res = vm.calculate_vehicle(
            current_tab.category,
            c['base'].currentData(),
            c['mission'].currentData(),
            c['motive'].currentData(),
            c['bulk'].currentData(),
            c['stage'].currentData(),
            c['desc'].currentData(),
            opt_idxs,
            c['end'].currentData()
        )
        self.render_result(res)

    def render_result(self, res):
        if not res: return
        self.res_name.setText(str(res.get("type", "Unknown")))
        self.res_type.setText(f"{self.tabs.tabText(self.tabs.currentIndex())} Vehicle")
        self.res_tl.setText(f"TL: {res.get('tl', '-')}")
        self.res_cost.setText(f"Cost: {res.get('kcr', '-')} KCr")
        self.res_mass.setText(f"Vol: {res.get('vol', '-')} tons")
        
        self.res_speed.setText(f"Speed: {res.get('spd', '-')}")
        self.res_load.setText(f"Load: {res.get('ld', '-')}")
        self.res_q.setText(f"Q: {res.get('q', '-')}")
        
        # Armour Values
        while self.res_pills.count():
            item = self.res_pills.takeAt(0)
            if item.widget(): item.widget().deleteLater()
            
        labels = {'ar':'Ar','ca':'Ca','fp':'Fp','rp':'Rp','sp':'Sp','ps':'Ps','in':'In','se':'Se'}
        row, col = 0, 0
        for k, label in labels.items():
            val = res.get(k, 0)
            lbl = QLabel(f"{label}: {val}")
            lbl.setStyleSheet(f"background-color: {Styles.BG_COLOR}; color: {Styles.WHITE_TEXT}; padding: 2px 6px; border: 1px solid {Styles.BORDER_COLOR}; border-radius: 4px; font-weight: bold;")
            self.res_pills.addWidget(lbl, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1
