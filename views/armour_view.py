import flet as ft
import travtools.armourmaker as am
import random
from views.components import glass_card, Styles

class ArmourView(ft.Row):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True, spacing=20)
        self.app_page = page
        
        # --- State ---
        self.am_selected_opts = set(am.STANDARD_SUBSYSTEMS.get("D", []))
        self.am_selected_drawbacks = {}
        self.last_am_type = "D"

        # --- Custom UI Elements ---
        self.am_type = ft.Dropdown(label="Armor Type", options=[ft.DropdownOption(key=k, text=f"{v['name']} (TL{v['tl']})") for k, v in am.TYPES.items() if v['type'] == 'System'], value="D")
        self.am_type.on_change = self.on_am_type_change
        
        self.am_desc = ft.Dropdown(label="Descriptor", options=[ft.DropdownOption(key=k, text=k or "(Blank)") for k in am.MODIFIERS["descriptor"].keys()], value="")
        self.am_desc.on_change = self.update_am_output_custom
        
        self.am_burden = ft.Dropdown(label="Burden", options=[ft.DropdownOption(key=k, text=k or "(Blank)") for k in am.MODIFIERS["burden"].keys()], value="")
        self.am_burden.on_change = self.update_am_output_custom
        
        self.am_stage = ft.Dropdown(label="Stage", options=[ft.DropdownOption(key=k, text=k or "(Blank)") for k in am.MODIFIERS["stage"].keys()], value="")
        self.am_stage.on_change = self.update_am_output_custom
        
        self.am_user = ft.Dropdown(label="User (Sophont)", options=[ft.DropdownOption(key=k, text=v['name']) for k, v in am.USERS.items()], value="")
        self.am_user.on_change = self.update_am_output_custom
        
        # --- Pre-made UI Elements ---
        self.am_pre_body = ft.Dropdown(label="Body Armor", options=[ft.DropdownOption(key=k, text=v["name"]) for k, v in am.TYPES.items() if v["category"] == "Body"])
        self.am_pre_body.on_change = self.on_premade_change
        
        self.am_pre_head = ft.Dropdown(label="Head Protection", options=[ft.DropdownOption(key=k, text=v["name"]) for k, v in am.TYPES.items() if v["category"] == "Head"])
        self.am_pre_head.on_change = self.on_premade_change
        
        self.am_pre_breath = ft.Dropdown(label="Breathers / Air", options=[ft.DropdownOption(key=k, text=v["name"]) for k, v in am.TYPES.items() if v["category"] == "Breather"])
        self.am_pre_breath.on_change = self.on_premade_change

        # Output Elements
        self.am_res_name = ft.Text("Battle Dress", size=28, weight=ft.FontWeight.BOLD, color=Styles.AMBER)
        self.am_res_model = ft.Text("BD-10", size=20, color=ft.Colors.WHITE70, italic=True)
        self.am_res_tl = ft.Text("TL: 10", size=16)
        self.am_res_cost = ft.Text("Cost: Cr 40,000", size=16)
        self.am_res_mass = ft.Text("Mass: 40 kg", size=16)
        self.am_res_qrebs = ft.Text("QREBS: 50000", size=16)
        self.am_res_pills = ft.Row(wrap=True, spacing=5)
        self.am_res_str = ft.Text("x10", size=16)
        self.am_res_dex = ft.Text("-2", size=16)
        self.am_res_end = ft.Text("-1", size=16)
        self.am_res_skill = ft.Text("BattleDress", size=16, color=ft.Colors.GREY_400)
        self.am_res_notes = ft.Column(spacing=2)

        # Subsystem UI Elements
        self.sub_cbs = {}
        self.sub_drawbacks = {}
        
        self.build_ui()
        
        # Initial Population to match HTML feel
        self.update_am_output_custom(None)

    def build_ui(self):
        # Accordion-style layout using ExpansionTiles
        # We group "Custom Setup" and "Pre-made" into separate Tiles to replace the glitchy buttons
        self.controls = [
            ft.Column([
                ft.ExpansionTile(
                    title=ft.Text("Custom Armour Design", size=18, weight=ft.FontWeight.W_500, color=Styles.AMBER),
                    controls=[
                        ft.Container(
                            content=ft.Column([
                                glass_card(ft.Column([self.am_type, self.am_desc, self.am_burden, self.am_stage, self.am_user], spacing=10), color=Styles.CARD_BG),
                                ft.Text("Subsystems", size=16, weight=ft.FontWeight.W_500, color=Styles.CYAN),
                                ft.Column([self.get_subsystem_category(cat) for cat in am.SUBSYSTEM_CATS.keys()], spacing=0)
                            ], spacing=15),
                            padding=10
                        )
                    ]
                ),
                ft.ExpansionTile(
                    title=ft.Text("Pre-made Armour Picker", size=18, weight=ft.FontWeight.W_500, color=Styles.BLUE),
                    controls=[
                        ft.Container(
                            content=glass_card(ft.Column([self.am_pre_body, self.am_pre_head, self.am_pre_breath], spacing=15), color=Styles.CARD_BG),
                            padding=10
                        )
                    ]
                )
            ], expand=True, scroll=ft.ScrollMode.AUTO),
            # Profile View (Right Side)
            ft.Column([
                glass_card(
                    ft.Column([
                        self.am_res_model, self.am_res_name,
                        ft.Divider(color=ft.Colors.WHITE10),
                        ft.Row([self.am_res_tl, self.am_res_cost, self.am_res_mass], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        self.am_res_qrebs,
                        self.am_res_pills,
                        ft.Divider(color=ft.Colors.WHITE10),
                        ft.Row([
                            ft.Column([ft.Text("STR", size=12, color=ft.Colors.GREY_400), self.am_res_str], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            ft.Column([ft.Text("DEX", size=12, color=ft.Colors.GREY_400), self.am_res_dex], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            ft.Column([ft.Text("END", size=12, color=ft.Colors.GREY_400), self.am_res_end], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                        self.am_res_skill,
                        ft.Divider(color=ft.Colors.WHITE10),
                        ft.Text("Features & Notes", size=18, weight=ft.FontWeight.W_500),
                        self.am_res_notes
                    ], spacing=10),
                    title="Armor Profile", color=Styles.GREEN, expand=True
                )
            ], expand=True)
        ]

    def get_subsystem_category(self, cat):
        ids = am.SUBSYSTEM_CATS.get(cat, [])
        cat_controls = []
        for opt_id in ids:
            v = next((o for o in am.OPTIONS if o["id"] == opt_id), None)
            if not v: continue
            cb = ft.Checkbox(label=v['name'], value=False, data=opt_id)
            cb.on_change = self.on_am_cb_change
            self.sub_cbs[opt_id] = cb
            db_text = ft.Text("", size=12, color=ft.Colors.RED_400, italic=True, visible=False)
            self.sub_drawbacks[opt_id] = db_text
            cat_controls.append(ft.Column([cb, db_text], spacing=0))
        return ft.ExpansionTile(title=ft.Text(cat.capitalize(), size=14), controls=cat_controls)

    def on_premade_change(self, e):
        self.update_am_output_premade()

    def refresh_subsystem_styles(self):
        standards = am.STANDARD_SUBSYSTEMS.get(self.am_type.value, [])
        for opt_id, cb in self.sub_cbs.items():
            v = next((o for o in am.OPTIONS if o["id"] == opt_id), None)
            is_std = opt_id in standards
            is_sel = opt_id in self.am_selected_opts
            cb.value = is_sel
            cb.label = f"{v['name']} (Standard)" if is_std else v['name']
            cb.label_style = ft.TextStyle(color=ft.Colors.GREEN_400 if is_std else ft.Colors.WHITE)
            db_text = self.sub_drawbacks[opt_id]
            if is_sel and not is_std and opt_id in self.am_selected_drawbacks:
                db_id = self.am_selected_drawbacks[opt_id]
                db_name = next((d['name'] for p in am.DRAWBACKS.values() for d in p if d['id'] == db_id), "Unknown")
                db_text.value = f"   ↳ {db_name}"; db_text.visible = True
            else:
                db_text.visible = False
        try: self.update()
        except: pass

    def on_am_cb_change(self, e):
        opt_id = e.control.data
        if e.control.value:
            self.am_selected_opts.add(opt_id)
            standards = am.STANDARD_SUBSYSTEMS.get(self.am_type.value, [])
            if opt_id not in standards:
                extras = [o for o in self.am_selected_opts if o not in standards]
                table_num = 1 if len(extras) == 1 else (2 + (len(extras)-2)%3)
                self.am_selected_drawbacks[opt_id] = random.choice(am.DRAWBACKS[table_num])["id"]
        else:
            self.am_selected_opts.discard(opt_id)
            self.am_selected_drawbacks.pop(opt_id, None)
        self.update_am_output_custom()
        self.refresh_subsystem_styles()

    def on_am_type_change(self, e):
        old_standards = set(am.STANDARD_SUBSYSTEMS.get(self.last_am_type, []))
        new_standards = set(am.STANDARD_SUBSYSTEMS.get(self.am_type.value, []))
        self.am_selected_opts = {opt for opt in self.am_selected_opts if opt not in old_standards}
        self.am_selected_opts.update(new_standards)
        for opt_id in list(self.am_selected_drawbacks.keys()):
            if opt_id in new_standards: del self.am_selected_drawbacks[opt_id]
        self.last_am_type = self.am_type.value
        self.update_am_output_custom()
        self.refresh_subsystem_styles()

    def update_am_output_custom(self, e=None):
        res = am.calculate_custom_armor(self.am_type.value, self.am_desc.value, self.am_burden.value, self.am_stage.value, self.am_user.value, list(self.am_selected_opts), self.am_selected_drawbacks)
        self.render_result(res, is_custom=True)

    def update_am_output_premade(self, e=None):
        res = am.calculate_premade_armor(self.am_pre_body.value, self.am_pre_head.value, self.am_pre_breath.value)
        self.render_result(res, is_custom=False)

    def render_result(self, res, is_custom):
        if not res:
            self.am_res_name.value = "No Selection"; self.am_res_model.value = "-"; self.am_res_tl.value = "TL: -"; self.am_res_cost.value = "Cost: -"; self.am_res_mass.value = "Mass: -"; self.am_res_qrebs.value = "QREBS: -"; self.am_res_pills.controls = []; self.am_res_str.value = "-"; self.am_res_dex.value = "-"; self.am_res_end.value = "-"; self.am_res_skill.value = "-"; self.am_res_notes.controls = []
        else:
            self.am_res_name.value = res["long_name"]; self.am_res_model.value = res["model"]; self.am_res_tl.value = f"TL: {res['tl']}"; self.am_res_cost.value = f"Cost: Cr {int(res['cost']):,}"; self.am_res_mass.value = f"Mass: {int(res['mass'])} kg"; self.am_res_qrebs.value = f"QREBS: {res['qrebs']}"
            self.am_res_pills.controls = []
            labels = {'ar':'Ar','ca':'Ca','fl':'Fl','ra':'Ra','so':'So','ps':'Ps','ins':'In','seal':'Se'}
            for k, v in res['stats'].items():
                if v > 0 or (k == 'ar' and v == 0):
                    self.am_res_pills.controls.append(ft.Container(content=ft.Text(f"{labels[k]}={v}", size=12, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD), padding=ft.Padding(10,5,10,5), bgcolor=ft.Colors.GREY_800, border_radius=5))
            ev = res['eval']
            self.am_res_str.value = f"x{ev['strMult']}" if ev['strMult'] != 1 else (str(ev['str']) if ev['str'] != 0 else "-")
            self.am_res_dex.value = f"{'+' if ev['dex']>0 else ''}{ev['dex']}" if ev['dex'] != 0 else "-"; self.am_res_end.value = "Stamina" if ev['stamina'] else (f"{'+' if ev['end']>0 else ''}{ev['end']}" if ev['end'] != 0 else "-"); self.am_res_skill.value = res['skill']
            self.am_res_notes.controls = []
            if is_custom:
                if res["standards"]: self.am_res_notes.controls.append(ft.Text(f"Standard: {', '.join(res['standards'])}", size=14, color=ft.Colors.GREEN_400))
                if res["extras"]: self.am_res_notes.controls.append(ft.Text(f"Additional: {', '.join(res['extras'])}", size=14, color=Styles.CYAN))
                if res["drawbacks"]: self.am_res_notes.controls.append(ft.Text(f"Drawbacks: {', '.join(res['drawbacks'])}", size=14, color=ft.Colors.RED_400, italic=True))
            else:
                self.am_res_notes.controls.append(ft.Text(res.get("notes", ""), size=14))
        try: self.update()
        except: pass
