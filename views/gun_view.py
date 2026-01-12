import flet as ft
import travtools.gunmaker as gm
import travtools.qrebs as qrebs_gen
import random
from views.components import glass_card, Styles

class GunView(ft.Row):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True, spacing=20)
        self.app_page = page
        
        # --- UI Elements ---
        self.gm_type_options = []
        for cat, types in gm.CHART_3_TYPES.items():
            for code, data in types.items():
                self.gm_type_options.append(ft.DropdownOption(key=f"{cat}|{code}", text=f"{cat}: {data['name']} (TL{data['tl']})"))

        self.gm_type = ft.Dropdown(label="Weapon Category & Type", options=self.gm_type_options, value="Handguns|P")
        self.gm_type.on_change = self.update_gm_desc
        
        self.gm_desc = ft.Dropdown(label="Descriptor")
        self.gm_desc.on_change = self.update_gm_output
        
        self.gm_user = ft.Dropdown(label="User (Sophont)", options=[ft.DropdownOption(key=k, text=v['name']) for k, v in gm.CHART_5_USER.items()], value="M")
        self.gm_user.on_change = self.update_gm_output
        
        self.gm_port = ft.Dropdown(label="Portability", value="auto", options=[ft.DropdownOption("auto", "Auto-Calculate"), ft.DropdownOption("Personal"), ft.DropdownOption("Crewed"), ft.DropdownOption("Fixed"), ft.DropdownOption("Portable"), ft.DropdownOption("Vehicle"), ft.DropdownOption("Turret")])
        self.gm_port.on_change = self.update_gm_output

        self.burden_cbs = {}
        self.gm_burdens = ft.Column(spacing=0)
        for k, v in gm.CHART_5_BURDEN.items():
            cb = ft.Checkbox(label=v['name'], value=False, data=k)
            cb.on_change = self.update_gm_output; self.burden_cbs[k] = cb; self.gm_burdens.controls.append(cb)
        
        self.stage_cbs = {}
        self.gm_stages = ft.Column(spacing=0)
        for k, v in gm.CHART_5_STAGE.items():
            cb = ft.Checkbox(label=v['name'], value=False, data=k)
            cb.on_change = self.update_gm_output; self.stage_cbs[k] = cb; self.gm_stages.controls.append(cb)

        self.option_cbs = {}
        self.gm_options = ft.Column(spacing=0)
        for k, v in gm.CHART_7_OPTIONS.items():
            cb = ft.Checkbox(label=v, value=False, data=k)
            cb.on_change = self.update_gm_output; self.option_cbs[k] = cb; self.gm_options.controls.append(cb)

        # Output Elements
        self.gm_res_model = ft.Text("Model", size=20, color=ft.Colors.WHITE70, italic=True)
        self.gm_res_name = ft.Text("Name", size=28, weight=ft.FontWeight.BOLD, color=Styles.AMBER)
        self.gm_res_stats = ft.Column(spacing=5)
        self.gm_res_effects = ft.Column(spacing=5)
        self.gm_res_controls = ft.Row(wrap=True, spacing=5)
        self.gm_res_options_list = ft.Column(spacing=2)
        self.gm_res_options_group = ft.Column([ft.Text("Options", size=18, weight=ft.FontWeight.W_500), self.gm_res_options_list], spacing=5, visible=False)
        self.gm_res_wx = ft.Text("Wx: ...", color=Styles.CYAN, selectable=True)
        self.gm_qrebs_result = ft.Column(spacing=5)
        self.gm_seed_input = ft.TextField(label="Seed", width=150, text_size=12, height=40, content_padding=10)
        
        self.gm_status = ft.Text("", size=12, color=ft.Colors.RED_400, italic=True)
        
        self.is_generated = False; self.latest_gm_burden = 0
        self.build_ui()
        
        # Initial Population to match HTML feel
        self.update_gm_desc(None)

    def build_ui(self):
        # Left Side: Setup and Modifications (Accordion)
        self.controls = [
            ft.Column([
                glass_card(ft.Column([self.gm_type, self.gm_desc, self.gm_user, self.gm_port], spacing=15), title="Weapon Core", color=Styles.AMBER),
                glass_card(
                    ft.Column([
                        ft.Text("Modifications", size=18, weight=ft.FontWeight.W_500),
                        ft.Divider(height=1, color=ft.Colors.WHITE10),
                        ft.ExpansionTile(title=ft.Text("Burden", size=14), controls=[ft.Container(self.gm_burdens, padding=10)]),
                        ft.ExpansionTile(title=ft.Text("Stage", size=14), controls=[ft.Container(self.gm_stages, padding=10)]),
                        ft.ExpansionTile(title=ft.Text("Options", size=14), controls=[ft.Container(self.gm_options, padding=10)]),
                    ]), color=Styles.CYAN
                ),
            ], expand=True, spacing=20, scroll=ft.ScrollMode.AUTO),
            # Right Side: Profile
            ft.Column([
                glass_card(ft.Column([self.gm_res_model, self.gm_res_name, ft.Divider(color=ft.Colors.WHITE10), self.gm_res_stats, ft.Text("Effects", size=18, weight=ft.FontWeight.W_500), self.gm_res_effects, ft.Text("Controls", size=18, weight=ft.FontWeight.W_500), self.gm_res_controls, self.gm_res_options_group, ft.Container(self.gm_res_wx, padding=15, bgcolor=ft.Colors.BLACK, border_radius=10, border=ft.Border.all(1, ft.Colors.WHITE10)), ft.Divider(color=ft.Colors.WHITE10), ft.Text("Production Quality", size=18, weight=ft.FontWeight.W_500), ft.Container(content=ft.Column([ft.Row([self.gm_seed_input, ft.FilledButton("Randomize", icon=ft.Icons.CASINO, on_click=self.randomize_gm_qrebs, expand=True)]), self.gm_qrebs_result], spacing=10), padding=10, bgcolor=ft.Colors.BLACK54, border_radius=10), self.gm_status], spacing=10), title="Weapon Profile", color=Styles.GREEN, expand=True)
            ], expand=True, spacing=20)
        ]

    def randomize_gm_qrebs(self, e):
        if not self.gm_seed_input.value: self.gm_seed_input.value = str(random.randint(0, 100000))
        self.is_generated = True; self.update_gm_output(None)

    def update_gm_desc(self, e):
        if not self.gm_type.value: return
        try:
            cat, code = self.gm_type.value.split("|")
            opts = [ft.DropdownOption(key=k, text=v['name'] or "(None)") for k, v in gm.CHART_4_DESCRIPTORS[cat].items()]
            self.gm_desc.options = opts
            if opts:
                self.gm_desc.value = opts[0].key # Auto-select first (None) descriptor
            else:
                self.gm_desc.value = ""
            try: self.gm_desc.update()
            except: pass
            self.update_gm_output(e)
        except Exception as err:
            self.gm_status.value = f"Load Error: {str(err)}"
            try: self.update()
            except: pass

    def update_gm_output(self, e):
        try:
            if not self.gm_type.value: return
            self.gm_status.value = ""
            cat, t_code = self.gm_type.value.split("|"); d_code = self.gm_desc.value; b_codes = [k for k, cb in self.burden_cbs.items() if cb.value]; s_codes = [k for k, cb in self.stage_cbs.items() if cb.value]; o_codes = [k for k, cb in self.option_cbs.items() if cb.value]
            res = gm.calculate_weapon(cat, t_code, d_code, b_codes, s_codes, self.gm_user.value, self.gm_port.value, o_codes)
            self.latest_gm_burden = res.get('qrebs_mod', 0); qrebs_display = res['qrebs']
            if self.is_generated:
                try:
                    q_res = qrebs_gen.generate_qrebs(seed=int(self.gm_seed_input.value), modifiers={'b': self.latest_gm_burden})
                    self.gm_qrebs_result.controls = [ft.Text(f"Instance Code: {q_res['code']}", size=20, weight=ft.FontWeight.BOLD, color=Styles.CYAN), ft.Text(q_res['text'], size=14, color=ft.Colors.GREY_300)]
                    qrebs_display = q_res['code']
                except ValueError: pass
            self.gm_res_model.value = res['model']; self.gm_res_name.value = res['long_name']; self.gm_res_stats.controls = [ft.Text(f"TL: {res['tl']}", size=16), ft.Text(f"Range: {res['range']}", size=16), ft.Text(f"Mass: {res['mass']:.2f} kg", size=16), ft.Text(f"Cost: Cr {int(res['cost']):,}", size=16), ft.Text(f"QREBS: {qrebs_display}", size=16, color=Styles.CYAN if self.is_generated else None)]
            self.gm_res_effects.controls = [ft.Text(f"{k}: {v}", size=14, color=ft.Colors.GREY_400) for k, v in res['effects'].items()]
            self.gm_res_controls.controls = []
            ctrl_labels = {"off": "Safe", "single": "Semi", "burst": "Burst", "full": "Auto", "p123": "1-2-3", "override": "Ovrd"}
            for k, v in res['controls'].items():
                if v: self.gm_res_controls.controls.append(ft.Container(content=ft.Text(ctrl_labels[k], size=12, color=Styles.AMBER), padding=5, border=ft.Border.all(1, ft.Colors.AMBER_700), border_radius=5, bgcolor=ft.Colors.BLACK54))
            self.gm_res_options_list.controls = [ft.Text(f"• {opt}", size=14, color=ft.Colors.GREY_400) for opt in res['options']]
            self.gm_res_options_group.visible = len(res['options']) > 0; eff_str = " ".join([f"{k}-{v}" for k, v in res['effects'].items()])
            self.gm_res_wx.value = f"Wx: R={res['range']} Cr{int(res['cost']):,} {res['mass']:.1f}kg B={res['base_qrebs']} {eff_str}"
            try: self.update()
            except: pass
        except Exception as err:
            self.gm_status.value = f"Calculation Error: {str(err)}"
            try: self.update()
            except: pass
