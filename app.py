import flet as ft
import math as m
import re
import travtools.commerce as cm
import travtools.system as ts
import travtools.dice as dd
import travtools.gunmaker as gm
import travtools.armourmaker as am
import travtools.qrebs as qrebs_gen
import random
from views.components import glass_card

class NumericSpinner(ft.Row):
    def __init__(self, label, value=0, min_val=0, max_val=15):
        super().__init__(spacing=5, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        self.min_val = min_val
        self.max_val = max_val
        self.text_field = ft.TextField(
            value=str(value),
            label=label,
            width=100,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self.validate
        )
        self.controls = [
            ft.IconButton(ft.Icons.REMOVE_CIRCLE_OUTLINE, on_click=self.minus_click, icon_size=20),
            self.text_field,
            ft.IconButton(ft.Icons.ADD_CIRCLE_OUTLINE, on_click=self.plus_click, icon_size=20),
        ]

    def minus_click(self, e):
        curr = int(self.text_field.value)
        if curr > self.min_val:
            self.text_field.value = str(curr - 1)
            self.update()

    def plus_click(self, e):
        curr = int(self.text_field.value)
        if curr < self.max_val:
            self.text_field.value = str(curr + 1)
            self.update()

    def validate(self, e):
        try:
            val = int(self.text_field.value)
            if val < self.min_val: self.text_field.value = str(self.min_val)
            if val > self.max_val: self.text_field.value = str(self.max_val)
        except:
            self.text_field.value = str(self.min_val)
            
    @property
    def value(self):
        return int(self.text_field.value)
    
    @value.setter
    def value(self, val):
        self.text_field.value = str(val)
        self.update()

    @property
    def value(self):
        try:
            return int(self.text_field.value)
        except:
            return self.min_val

def main(page: ft.Page):
    page.title = "StarBright - Traveller Utility"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0B0E14" # Deep space dark
    page.window.width = 1100
    page.window.height = 850
    
    # --- Glassmorphism Style Helpers ---
    glass_bg = ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
    glass_border = ft.Border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE))
    glass_blur = 15

    
    # --- State and Logic ---
    uwp_pat = re.compile('[ABCDEXFGHY][0-9A-F][0-9A-F][0-9A][0-9A-F][0-9A-F][0-9A-J]-[0-9A-J]')
    
    # --- Trade: Buy UI Elements ---
    buy_uwp = ft.TextField(label="UWP (e.g., A110877-E)", border_color=ft.Colors.BLUE_400, expand=True)
    buy_steward = NumericSpinner("Steward", value=0)
    buy_admin = NumericSpinner("Admin", value=0)
    buy_street = NumericSpinner("Streetwise", value=0)
    buy_liaison = NumericSpinner("Liaison", value=0)
    buy_days = NumericSpinner("Days", value=7, min_val=1, max_val=14)
    buy_result = ft.Text(selectable=True)
    
    def on_buy_click(e):
        buy_result.value = ""
        uwp = buy_uwp.value.upper()
        if not uwp:
            buy_result.value = "Error: No UWP Provided."
        elif len(uwp) != 9:
            buy_result.value = "Error: Incorrect length UWP (should be 9 chars)."
        elif not uwp_pat.match(uwp):
            buy_result.value = "Error: Incorrect UWP pattern."
        else:
            try:
                skills = {
                    'Steward': buy_steward.value,
                    'Admin': buy_admin.value,
                    'Streetwise': buy_street.value,
                    'Liaison': buy_liaison.value
                }
                trade_data = cm.trade_gds(uwp, skills, buy_days.value)
                buy_result.value = trade_data if trade_data else "No goods found / Error in calculation."
            except Exception as ex:
                buy_result.value = f"Error: {str(ex)}"
        page.update()

    # --- Trade: Sell UI Elements ---
    sell_cargo = ft.TextField(label="Cargo ID (e.g., B - Ri Cr5,100)", border_color=ft.Colors.GREEN_400)
    sell_uwp = ft.TextField(label="Destination UWP", border_color=ft.Colors.GREEN_400)
    sell_broker = ft.Dropdown(label="Broker Skill", options=[ft.DropdownOption(str(i)) for i in range(16)], value="0")
    sell_trade_roll = ft.Dropdown(label="Trade pre-roll (optional)", options=[ft.DropdownOption(str(i)) for i in range(1, 7)], value="0")
    sell_result = ft.Text(selectable=True)

    def on_sell_click(e):
        sell_result.value = ""
        uwp = sell_uwp.value.upper()
        cargo = sell_cargo.value
        if not cargo:
            sell_result.value = "Error: No Cargo Code entered."
        elif len(uwp) != 9:
            sell_result.value = "Error: Incorrect length UWP."
        elif not uwp_pat.match(uwp):
            sell_result.value = "Error: Incorrect UWP Pattern."
        else:
            try:
                trd = int(sell_trade_roll.value) if sell_trade_roll.value else 0
                broker = int(sell_broker.value)
                value = cm.sell_price(cargo, uwp, broker, trd)
                if value > 0:
                    sell_result.value = f"Sell Price: Cr{value:,}"
                else:
                    sell_result.value = "No value found / Error in calculation."
            except Exception as ex:
                sell_result.value = f"Error: {str(ex)}"
        page.update()

    # --- Travel Time UI Elements ---
    travel_adia = ft.TextField(label="Departure / Arrival Diameters", value="100", keyboard_type=ft.KeyboardType.NUMBER)
    travel_pdia = ft.TextField(label="Planet Diameter (km)", value="5000", keyboard_type=ft.KeyboardType.NUMBER)
    travel_spd = ft.TextField(label="Speed of Ship (G)", value="1", keyboard_type=ft.KeyboardType.NUMBER)
    travel_result = ft.Text()

    def on_travel_click(e):
        try:
            a_dia = float(travel_adia.value) if travel_adia.value else 0
            p_dia = float(travel_pdia.value) if travel_pdia.value else 0
            s_spd = float(travel_spd.value) if travel_spd.value else 0
            # Time in hours: sqrt( (2*d) / a ) -> simplified calculation variant
            # This is a rough estimation for Traveller play
            time = m.sqrt((a_dia * p_dia) / (s_spd * 32400))
            hr = int(time)
            mins = int((time - hr) * 60)
            travel_result.value = f"Estimated travel time: {hr} hours and {mins} minutes"
        except Exception as ex:
            travel_result.value = f"Error: {str(ex)}"
        page.update()

    # --- System Generator UI Elements ---
    sys_seed = ft.TextField(label="System Seed (Number)", value="12345", keyboard_type=ft.KeyboardType.NUMBER, expand=True)
    sys_result = ft.Column(spacing=10)

    def on_random_seed_click(e):
        sys_seed.value = str(random.randint(1000, 999999))
        page.update()

    def on_sys_gen_click(e):
        try:
            seed = int(sys_seed.value) if sys_seed.value else 0
            uwp = ts.fun_uwp(seed)
            pbg = ts.fun_pbg(uwp)
            bases = ts.fun_bases(uwp)
            trade = ts.fun_trade(uwp)
            ext = ts.fun_ext(uwp, pbg, bases, trade)
            
            sys_result.controls = [
                ft.Text(f"UWP: {uwp}", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER),
                ft.Text(f"PBG: {pbg}", size=18, color=ft.Colors.WHITE70),
                ft.Text(f"Bases: {bases if bases else 'None'}", size=18, color=ft.Colors.WHITE70),
                ft.Text(f"Trade Codes: {trade}", size=18, color=ft.Colors.CYAN_200),
                ft.Text(f"Extensions: {ext}", size=20, weight=ft.FontWeight.W_500, color=ft.Colors.PURPLE_200),
            ]
        except Exception as ex:
            sys_result.controls = [ft.Text(f"Error: {str(ex)}", color=ft.Colors.RED_400)]
        page.update()

    # --- GunMaker UI Elements & Logic ---
    gm_type_options = []
    for cat, types in gm.CHART_3_TYPES.items():
        for code, data in types.items():
            gm_type_options.append(ft.DropdownOption(key=f"{cat}|{code}", text=f"{cat}: {data['name']} (TL{data['tl']})"))

    gm_res_model = ft.Text("Model", size=20, color=ft.Colors.WHITE70, italic=True)
    gm_res_name = ft.Text("Name", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER)
    gm_res_stats = ft.Column(spacing=5)
    gm_res_effects = ft.Column(spacing=5)
    gm_res_controls = ft.Row(wrap=True, spacing=5)
    gm_res_options_list = ft.Column(spacing=2)
    gm_res_options_group = ft.Column([
        ft.Text("Options", size=18, weight=ft.FontWeight.W_500),
        gm_res_options_list
    ], spacing=5, visible=False)
    gm_res_wx = ft.Text("Wx: ...", color=ft.Colors.CYAN_200, selectable=True)
    
    gm_qrebs_result = ft.Column(spacing=5)
    gm_seed_input = ft.TextField(label="Seed", width=150, text_size=12, height=40, content_padding=10)
    
    burden_cbs = {}
    stage_cbs = {}
    option_cbs = {}
    
    # State tracking
    is_generated = [False]
    latest_gm_burden = [0] 

    def randomize_gm_qrebs(e):
        import numpy as np
        # Generate new seed if empty or explicitly requested (logic could handle "empty" as request for new)
        # Here we just check validity. If the user cleared it, we make a new one.
        if not gm_seed_input.value:
            gm_seed_input.value = str(list(np.random.randint(0, 100000, 1))[0])
        
        is_generated[0] = True
        update_gm_output(None)

    def update_gm_output(e):
        if not gm_type.value: return
        cat, t_code = gm_type.value.split("|")
        d_code = gm_desc.value
        b_codes = [k for k, cb in burden_cbs.items() if cb.value]
        s_codes = [k for k, cb in stage_cbs.items() if cb.value]
        o_codes = [k for k, cb in option_cbs.items() if cb.value]
        
        res = gm.calculate_weapon(cat, t_code, d_code, b_codes, s_codes, gm_user.value, gm_port.value, o_codes)
        
        # Update latest burden
        latest_gm_burden[0] = res.get('qrebs_mod', 0)
        
        # QREBS Logic
        qrebs_display = res['qrebs']
        
        if is_generated[0]:
            try:
                seed_val = int(gm_seed_input.value)
                q_res = qrebs_gen.generate_qrebs(seed=seed_val, modifiers={'b': latest_gm_burden[0]})
                
                # Update QREBS Result View
                gm_qrebs_result.controls = [
                    ft.Text(f"Instance Code: {q_res['code']}", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_200),
                    ft.Text(q_res['text'], size=14, color=ft.Colors.GREY_300)
                ]
                
                # Override display value
                qrebs_display = q_res['code']
            except ValueError:
                pass # Invalid seed, skip update
        
        gm_res_model.value = res['model']
        gm_res_name.value = res['long_name']
        gm_res_stats.controls = [
            ft.Text(f"TL: {res['tl']}", size=16),
            ft.Text(f"Range: {res['range']}", size=16),
            ft.Text(f"Mass: {res['mass']:.2f} kg", size=16),
            ft.Text(f"Cost: Cr {int(res['cost']):,}", size=16),
            ft.Text(f"QREBS: {qrebs_display}", size=16, color=ft.Colors.CYAN_200 if is_generated[0] else None),
        ]
        
        gm_res_effects.controls = [ft.Text(f"{k}: {v}", size=14, color=ft.Colors.GREY_400) for k, v in res['effects'].items()]
        
        gm_res_controls.controls = []
        ctrl_labels = {"off": "Safe", "single": "Semi", "burst": "Burst", "full": "Auto", "p123": "1-2-3", "override": "Ovrd"}
        for k, v in res['controls'].items():
            if v:
                gm_res_controls.controls.append(ft.Container(
                    content=ft.Text(ctrl_labels[k], size=12, color=ft.Colors.AMBER_200),
                    padding=5, border=ft.Border.all(1, ft.Colors.AMBER_700), border_radius=5, bgcolor=ft.Colors.BLACK54
                ))
        
        gm_res_options_list.controls = [ft.Text(f"• {opt}", size=14, color=ft.Colors.GREY_400) for opt in res['options']]
        gm_res_options_group.visible = len(res['options']) > 0
        
        eff_str = " ".join([f"{k}-{v}" for k, v in res['effects'].items()])
        gm_res_wx.value = f"Wx: R={res['range']} Cr{int(res['cost']):,} {res['mass']:.1f}kg B={qrebs_display} {eff_str}"
        page.update()

    def update_gm_desc(e):
        if not gm_type.value: return
        cat, code = gm_type.value.split("|")
        gm_desc.options = [ft.DropdownOption(key=k, text=v['name'] or "(None)") for k, v in gm.CHART_4_DESCRIPTORS[cat].items()]
        gm_desc.value = ""
        page.update()
        update_gm_output(e)

    gm_type = ft.Dropdown(label="Weapon Category & Type", options=gm_type_options)
    gm_type.on_select = update_gm_desc

    gm_desc = ft.Dropdown(label="Descriptor", options=[])
    gm_desc.on_select = update_gm_output

    gm_user = ft.Dropdown(label="User (Sophont)", options=[ft.DropdownOption(key=k, text=v['name']) for k, v in gm.CHART_5_USER.items()], value="M")
    gm_user.on_select = update_gm_output

    gm_port = ft.Dropdown(label="Portability", value="auto", options=[
        ft.DropdownOption("auto", "Auto-Calculate"),
        ft.DropdownOption("Personal"), ft.DropdownOption("Crewed"),
        ft.DropdownOption("Fixed"), ft.DropdownOption("Portable"),
        ft.DropdownOption("Vehicle"), ft.DropdownOption("Turret")
    ])
    gm_port.on_select = update_gm_output

    gm_burdens = ft.Column(spacing=0, scroll=ft.ScrollMode.AUTO)
    for k, v in gm.CHART_5_BURDEN.items():
        cb = ft.Checkbox(label=v['name'], value=False)
        cb.on_change = update_gm_output
        burden_cbs[k] = cb
        gm_burdens.controls.append(cb)
    
    gm_stages = ft.Column(spacing=0, scroll=ft.ScrollMode.AUTO)
    for k, v in gm.CHART_5_STAGE.items():
        cb = ft.Checkbox(label=v['name'], value=False)
        cb.on_change = update_gm_output
        stage_cbs[k] = cb
        gm_stages.controls.append(cb)

    gm_options = ft.Column(spacing=0, scroll=ft.ScrollMode.AUTO)
    for k, v in gm.CHART_7_OPTIONS.items():
        cb = ft.Checkbox(label=v, value=False)
        cb.on_change = update_gm_output
        option_cbs[k] = cb
        gm_options.controls.append(cb)

    # --- Layout Views ---
    def get_buy_view():
        return ft.Column([
            glass_card(
                ft.Column([
                    ft.Row([buy_uwp, buy_days], spacing=20),
                    ft.Text("Character Skills", size=16, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE70),
                    ft.Row([
                        buy_steward, buy_admin, buy_street, buy_liaison
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.FilledButton(
                        "Generate Goods", 
                        icon=ft.Icons.SEARCH, 
                        on_click=on_buy_click,
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.BLUE_700,
                        ),
                        height=50,
                        width=250
                    ),
                ], spacing=20),
                title="Speculative Trade: Buy",
                subtitle="Search for available goods to purchase.",
                color=ft.Colors.BLUE_300
            ),
            ft.Container(
                content=buy_result,
                padding=20,
                border_radius=15,
                bgcolor=ft.Colors.BLACK54,
                border=ft.Border.all(1, ft.Colors.BLUE_900),
                margin=ft.Margin.only(top=10),
                expand=True
            )
        ], expand=True, spacing=20)

    def get_sell_view():
        return ft.Column([
            glass_card(
                ft.Column([
                    sell_cargo,
                    sell_uwp,
                    ft.ResponsiveRow([
                        sell_broker, sell_trade_roll
                    ], spacing=10),
                    ft.FilledButton(
                        "Calculate Sale Price", 
                        icon=ft.Icons.MONEY, 
                        on_click=on_sell_click,
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.GREEN_700,
                        ),
                        height=50,
                        width=250
                    ),
                ], spacing=20),
                title="Speculative Trade: Sell",
                subtitle="Estimate the best market value for your cargo.",
                color=ft.Colors.GREEN_300
            ),
            ft.Container(
                content=sell_result,
                padding=20,
                border_radius=15,
                bgcolor=ft.Colors.BLACK54,
                border=ft.Border.all(1, ft.Colors.GREEN_900),
                margin=ft.Margin.only(top=10),
            )
        ], expand=True, spacing=20)

    def get_travel_view():
        return ft.Column([
            glass_card(
                ft.Column([
                    travel_adia,
                    travel_pdia,
                    travel_spd,
                    ft.FilledButton(
                        "Calculate Time", 
                        icon=ft.Icons.TIMER, 
                        on_click=on_travel_click,
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.ORANGE_700,
                        ),
                        height=50,
                        width=250
                    ),
                ], spacing=20),
                title="Travel Time",
                subtitle="Calculate hours between jumps and planets.",
                color=ft.Colors.ORANGE_300
            ),
            ft.Container(
                content=travel_result,
                padding=20,
                border_radius=15,
                bgcolor=ft.Colors.BLACK54,
                border=ft.Border.all(1, ft.Colors.ORANGE_900),
                margin=ft.Margin.only(top=10),
            )
        ], expand=True, spacing=20)

    def get_gm_view():
        # Custom Tab Switcher for Flet 0.8.0
        mod_switcher = ft.Container(gm_burdens, padding=10, height=300)
        
        def switch_mod_tab(e):
            if e.control.data == "Burden":
                mod_switcher.content = gm_burdens
                btn_burden.style = ft.ButtonStyle(bgcolor=ft.Colors.CYAN_700)
                btn_stage.style = None
                btn_options.style = None
            elif e.control.data == "Stage":
                mod_switcher.content = gm_stages
                btn_burden.style = None
                btn_stage.style = ft.ButtonStyle(bgcolor=ft.Colors.CYAN_700)
                btn_options.style = None
            else:
                mod_switcher.content = gm_options
                btn_burden.style = None
                btn_stage.style = None
                btn_options.style = ft.ButtonStyle(bgcolor=ft.Colors.CYAN_700)
            page.update()

        btn_burden = ft.TextButton("Burden", data="Burden", on_click=switch_mod_tab, style=ft.ButtonStyle(bgcolor=ft.Colors.CYAN_700))
        btn_stage = ft.TextButton("Stage", data="Stage", on_click=switch_mod_tab)
        btn_options = ft.TextButton("Options", data="Options", on_click=switch_mod_tab)

        mod_tabs = ft.Column([
            ft.Row([btn_burden, btn_stage, btn_options], spacing=5),
            ft.Divider(height=1, color=ft.Colors.WHITE10),
            mod_switcher
        ])

        return ft.Row([
            ft.Column([
                glass_card(
                    ft.Column([
                        gm_type, gm_desc, gm_user, gm_port
                    ], spacing=15),
                    title="Weapon Core", color=ft.Colors.AMBER_400
                ),
                glass_card(
                    mod_tabs,
                    title="Modifications", color=ft.Colors.CYAN_400
                ),
            ], expand=True, spacing=20, scroll=ft.ScrollMode.AUTO),
            ft.Column([
                glass_card(
                    ft.Column([
                        gm_res_model,
                        gm_res_name,
                        ft.Divider(color=ft.Colors.WHITE10),
                        gm_res_stats,
                        ft.Text("Effects", size=18, weight=ft.FontWeight.W_500),
                        gm_res_effects,
                        ft.Text("Controls", size=18, weight=ft.FontWeight.W_500),
                        gm_res_controls,
                        gm_res_options_group,
                        ft.Container(gm_res_wx, padding=15, bgcolor=ft.Colors.BLACK, border_radius=10, border=ft.Border.all(1, ft.Colors.WHITE10)),
                        ft.Divider(color=ft.Colors.WHITE10),
                        ft.Text("Production Quality", size=18, weight=ft.FontWeight.W_500),
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    gm_seed_input,
                                    ft.FilledButton("Randomize", icon=ft.Icons.CASINO, on_click=randomize_gm_qrebs, expand=True),
                                ]),
                                gm_qrebs_result
                            ], spacing=10),
                            padding=10, bgcolor=ft.Colors.BLACK54, border_radius=10
                        )
                    ], spacing=10),
                    title="Weapon Profile", color=ft.Colors.GREEN_400
                )
            ], expand=True, spacing=20)
        ], expand=True, spacing=20)
    
    # --- ArmourMaker UI Elements & Logic ---
    am_type = ft.Dropdown(label="Armor Type", options=[ft.DropdownOption(key=k, text=f"{v['name']} (TL{v['tl']})") for k, v in am.TYPES.items() if v['type'] == 'System'], value="D")
    am_desc = ft.Dropdown(label="Descriptor", options=[ft.DropdownOption(key=k, text=k or "(Blank)") for k in am.MODIFIERS["descriptor"].keys()], value="")
    am_burden = ft.Dropdown(label="Burden", options=[ft.DropdownOption(key=k, text=k or "(Blank)") for k in am.MODIFIERS["burden"].keys()], value="")
    am_stage = ft.Dropdown(label="Stage", options=[ft.DropdownOption(key=k, text=k or "(Blank)") for k in am.MODIFIERS["stage"].keys()], value="")
    am_user = ft.Dropdown(label="User (Sophont)", options=[ft.DropdownOption(key=k, text=v['name']) for k, v in am.USERS.items()], value="")
    
    am_pre_body = ft.Dropdown(label="Body Armor", options=[ft.DropdownOption(key=k, text=v["name"]) for k, v in am.TYPES.items() if v["category"] == "Body"])
    am_pre_head = ft.Dropdown(label="Head Protection", options=[ft.DropdownOption(key=k, text=v["name"]) for k, v in am.TYPES.items() if v["category"] == "Head"])
    am_pre_breath = ft.Dropdown(label="Breathers / Air", options=[ft.DropdownOption(key=k, text=v["name"]) for k, v in am.TYPES.items() if v["category"] == "Breather"])

    # Output Elements
    am_res_name = ft.Text("Battle Dress", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER)
    am_res_model = ft.Text("BD-10", size=20, color=ft.Colors.WHITE70, italic=True)
    am_res_tl = ft.Text("TL: 10", size=16)
    am_res_cost = ft.Text("Cost: Cr 40,000", size=16)
    am_res_mass = ft.Text("Mass: 40 kg", size=16)
    am_res_qrebs = ft.Text("QREBS: 50000", size=16)
    am_res_pills = ft.Row(wrap=True, spacing=5)
    am_res_str = ft.Text("x10", size=16)
    am_res_dex = ft.Text("-2", size=16)
    am_res_end = ft.Text("-1", size=16)
    am_res_skill = ft.Text("BattleDress", size=16, color=ft.Colors.GREY_400)
    am_res_notes = ft.Column(spacing=2)
    
    am_selected_opts = set(am.STANDARD_SUBSYSTEMS.get("D", []))
    am_selected_drawbacks = {}
    am_mode = "custom"
    am_current_sub_cat = "comms"
    am_sub_cbs = {}
    last_am_type = "D"

    def get_qrebs_view():
        # --- Generator Tab Content ---
        # Use ListView for better performance/reliability with lists
        gen_output = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, height=400)
        gen_qty = NumericSpinner("Quantity", value=1, min_val=1, max_val=20)
        
        def on_generate_qrebs(e):
            try:
                count = int(gen_qty.value)
                gen_output.controls.clear()
                
                new_controls = []
                for i in range(count):
                    res = qrebs_gen.generate_qrebs(seed=None)
                    
                    card = ft.ExpansionTile(
                        title=ft.Text(f"Code: {res['code']}", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_200),
                        subtitle=ft.Text("Click to see details", size=12, color=ft.Colors.GREY_500),
                        controls=[
                            ft.Container(
                                content=ft.Text(res['text'], size=14, color=ft.Colors.GREY_300),
                                padding=15, bgcolor=ft.Colors.BLACK54,
                                border_radius=10
                            )
                        ],
                        expanded= (count == 1),
                        collapsed_text_color=ft.Colors.WHITE,
                        text_color=ft.Colors.CYAN_100
                    )
                    new_controls.append(card)
                
                gen_output.controls = new_controls
                gen_output.update() 
                page.update()
            except Exception as ex:
                gen_output.controls = [ft.Text(f"Error: {ex}", color=ft.Colors.RED)]
                gen_output.update()
            
        gen_view = ft.Column([
            glass_card(
                ft.Column([
                    ft.Text("Batch Generator", size=20, weight=ft.FontWeight.BOLD),
                    ft.Row([gen_qty, ft.FilledButton("Generate", icon=ft.Icons.AUTO_AWESOME, on_click=on_generate_qrebs)]),
                    ft.Divider(color=ft.Colors.WHITE10),
                    gen_output
                ]),
                title="QREBS Generator", color=ft.Colors.PURPLE_400
            )
        ], visible=False) 

        # --- Decoder Tab Content ---
        dec_input = ft.TextField(label="Enter QREBS Code (e.g. 52364)", max_length=5, text_style=ft.TextStyle(letter_spacing=2))
        dec_output = ft.Column()
        
        def on_decode_qrebs(e):
            try:
                code = dec_input.value.upper()
                
                if len(code) != 5:
                    dec_output.controls = [ft.Text("Please enter a 5-character code.", color=ft.Colors.RED_400)]
                else:
                    res = qrebs_gen.decode_qrebs(code)
                    
                    if res['valid']:
                        dec_output.controls = [
                            ft.Container(
                                content=ft.Text(res['text'], size=16),
                                padding=20,
                                border=ft.Border.all(1, ft.Colors.GREEN_400),
                                border_radius=10,
                                bgcolor=ft.Colors.BLACK54
                            )
                        ]
                    else:
                        dec_output.controls = [ft.Text(res['text'], color=ft.Colors.RED_400)]
                
                dec_output.update() 
                page.update()
            except Exception as ex:
                dec_output.controls = [ft.Text(f"Error: {ex}", color=ft.Colors.RED)]
                dec_output.update()
            
        dec_view = ft.Column([
            glass_card(
                ft.Column([
                    ft.Text("Code Decoder", size=20, weight=ft.FontWeight.BOLD),
                    ft.Row([dec_input, ft.FilledButton("Decode", icon=ft.Icons.TRANSLATE, on_click=on_decode_qrebs)]),
                    ft.Divider(color=ft.Colors.WHITE10),
                    dec_output
                ]),
                title="QREBS Decoder", color=ft.Colors.TEAL_400
            )
        ], visible=True) 
        
        # --- Custom Switcher ---
        def switch_tab(e):
            try:
                if e.control.data == "gen":
                    gen_view.visible = True
                    dec_view.visible = False
                    btn_gen.style = ft.ButtonStyle(bgcolor=ft.Colors.PURPLE_700)
                    btn_dec.style = None
                else:
                    gen_view.visible = False
                    dec_view.visible = True
                    btn_gen.style = None
                    btn_dec.style = ft.ButtonStyle(bgcolor=ft.Colors.TEAL_700)
                
                gen_view.update()
                dec_view.update()
                page.update()
            except Exception as ex:
                pass

        btn_gen = ft.FilledButton("Generate", icon=ft.Icons.ADD_BOX_OUTLINED, data="gen", on_click=switch_tab)
        btn_dec = ft.FilledButton("Decode", icon=ft.Icons.QR_CODE_SCANNER, data="dec", on_click=switch_tab, style=ft.ButtonStyle(bgcolor=ft.Colors.TEAL_700))

        return ft.Column([
            ft.Row([btn_gen, btn_dec], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(color=ft.Colors.WHITE10),
            gen_view,
            dec_view
        ], expand=True)
    def get_am_view():
        nonlocal am_selected_opts, am_selected_drawbacks, am_mode, am_current_sub_cat
        am_core_card = None
        am_sub_card = None

        def update_am_output(e=None):
            if am_mode == "custom":
                res = am.calculate_custom_armor(am_type.value, am_desc.value, am_burden.value, am_stage.value, am_user.value, list(am_selected_opts), am_selected_drawbacks)
            else:
                res = am.calculate_premade_armor(am_pre_body.value, am_pre_head.value, am_pre_breath.value)
            
            if not res:
                am_res_name.value = "No Armor Selected"
                am_res_model.value = "-"
                am_res_tl.value = "TL: -"
                am_res_cost.value = "Cost: -"
                am_res_mass.value = "Mass: -"
                am_res_qrebs.value = "QREBS: -"
                am_res_pills.controls = []
                am_res_str.value = "-"
                am_res_dex.value = "-"
                am_res_end.value = "-"
                am_res_skill.value = "-"
                am_res_notes.controls = []
                page.update()
                return
                
            am_res_name.value = res["long_name"]
            am_res_model.value = res["model"]
            am_res_tl.value = f"TL: {res['tl']}"
            am_res_cost.value = f"Cost: Cr {int(res['cost']):,}"
            am_res_mass.value = f"Mass: {int(res['mass'])} kg"
            am_res_qrebs.value = f"QREBS: {res['qrebs']}"
            
            am_res_pills.controls = []
            labels = { 'ar':'Ar', 'ca':'Ca', 'fl':'Fl', 'ra':'Ra', 'so':'So', 'ps':'Ps', 'ins':'In', 'seal':'Se' }
            for k, v in res['stats'].items():
                if v > 0 or (k == 'ar' and v == 0):
                    am_res_pills.controls.append(ft.Container(
                        content=ft.Text(f"{labels[k]}={v}", size=12, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                        padding=ft.Padding(10, 5, 10, 5), bgcolor=ft.Colors.GREY_800, border_radius=5
                    ))
            
            ev = res['eval']
            str_val = f"x{ev['strMult']}" if ev['strMult'] != 1 else (str(ev['str']) if ev['str'] != 0 else "-")
            am_res_str.value = str_val
            am_res_dex.value = f"{'+' if ev['dex']>0 else ''}{ev['dex']}" if ev['dex'] != 0 else "-"
            am_res_end.value = "Stamina" if ev['stamina'] else (f"{'+' if ev['end']>0 else ''}{ev['end']}" if ev['end'] != 0 else "-")
            am_res_skill.value = res['skill']
            
            am_res_notes.controls = []
            if am_mode == "custom":
                if res["standards"]:
                    am_res_notes.controls.append(ft.Text(f"Standard: {', '.join(res['standards'])}", size=14, color=ft.Colors.GREEN_400))
                if res["extras"]:
                    am_res_notes.controls.append(ft.Text(f"Additional: {', '.join(res['extras'])}", size=14, color=ft.Colors.CYAN_400))
                if res["drawbacks"]:
                    am_res_notes.controls.append(ft.Text(f"Drawbacks: {', '.join(res['drawbacks'])}", size=14, color=ft.Colors.RED_400, italic=True))
            else:
                am_res_notes.controls.append(ft.Text(res.get("notes", ""), size=14))
                
            page.update()

        def on_am_type_change(e):
            nonlocal am_selected_opts, last_am_type
            # 1. Identify what WAS standard for the previous type
            old_standards = set(am.STANDARD_SUBSYSTEMS.get(last_am_type, []))
            # 2. Identify what IS standard for the new type
            new_standards = set(am.STANDARD_SUBSYSTEMS.get(am_type.value, []))
            
            # 3. Only remove things that WERE standard for the OLD type
            # (Keep anything the user manually added as an extra)
            am_selected_opts = {opt for opt in am_selected_opts if opt not in old_standards}
            
            # 4. Add the NEW standards
            am_selected_opts.update(new_standards)
            
            # 5. Remove drawbacks for anything that is now standard
            for opt_id in list(am_selected_drawbacks.keys()):
                if opt_id in new_standards:
                    del am_selected_drawbacks[opt_id]
            
            # Update tracking
            last_am_type = am_type.value
            
            # Update UI state for currently visible checkboxes
            for k, cb in am_sub_cbs.items():
                cb.value = k in am_selected_opts
            
            update_am_output()
            switch_sub_tab(am_current_sub_cat)

        def on_am_cb_change(e):
            opt_id = e.control.data
            if e.control.value:
                am_selected_opts.add(opt_id)
                standards = am.STANDARD_SUBSYSTEMS.get(am_type.value, [])
                if opt_id not in standards:
                    # Counting existing extras (including the one just added)
                    extras = [o for o in am_selected_opts if o not in standards]
                    count = len(extras)
                    if count == 1:
                        table_num = 1
                    else:
                        table_num = 2 + (count - 2) % 3
                    
                    db_pool = am.DRAWBACKS[table_num]
                    am_selected_drawbacks[opt_id] = random.choice(db_pool)["id"]
            else:
                am_selected_opts.discard(opt_id)
                if opt_id in am_selected_drawbacks:
                    del am_selected_drawbacks[opt_id]
            
            update_am_output()
            switch_sub_tab(am_current_sub_cat)
        # Subsystem Tabs
        sub_tab_container = ft.Column(scroll=ft.ScrollMode.AUTO, height=400)
        
        def switch_sub_tab(cat):
            nonlocal am_current_sub_cat
            am_current_sub_cat = cat
            controls = []
            standards = am.STANDARD_SUBSYSTEMS.get(am_type.value, [])
            for opt_id in am.SUBSYSTEM_CATS[cat]:
                opt_data = next(o for o in am.OPTIONS if o["id"] == opt_id)
                cb = ft.Checkbox(
                    label=f"{opt_data['name']} ({opt_data['desc']})", 
                    value=opt_id in am_selected_opts, 
                    data=opt_id, 
                    on_change=on_am_cb_change,
                    disabled=(am_mode == "premade")
                )
                am_sub_cbs[opt_id] = cb
                controls.append(cb)
                
                if opt_id in am_selected_drawbacks:
                    all_dbs = [item for sublist in am.DRAWBACKS.values() for item in sublist]
                    db_data = next((d for d in all_dbs if d["id"] == am_selected_drawbacks[opt_id]), None)
                    if db_data:
                        controls.append(ft.Container(
                            content=ft.Text(f"Drawback: {db_data['name']} ({db_data['desc']})", size=12, color=ft.Colors.RED_300, italic=True),
                            padding=ft.Padding(30, 0, 0, 10)
                        ))
            
            sub_tab_container.controls = controls
            for b in sub_btns: b.style = ft.ButtonStyle(bgcolor=ft.Colors.BLUE_700 if b.data == cat else None)
            page.update()

        def on_sub_tab_click(e):
            switch_sub_tab(e.control.data)
        sub_btns = [ft.TextButton(c.capitalize(), data=c, on_click=on_sub_tab_click) for c in am.SUBSYSTEM_CATS.keys()]
        
        # Initial sub-tab
        switch_sub_tab("comms")

        # Main Switcher (Custom / Premade)
        am_panels = ft.Column([
            ft.Text("Core Configuration", size=20, weight=ft.FontWeight.BOLD),
            am_type, am_desc, am_burden, am_stage, am_user
        ], spacing=10)
        
        def switch_am_mode(e):
            nonlocal am_mode
            am_mode = e.control.data.lower()
            if am_mode == "custom":
                btn_custom.style = ft.ButtonStyle(bgcolor=ft.Colors.BLUE_700)
                btn_premade.style = None
                am_panels.controls = [
                    ft.Text("Core Configuration", size=20, weight=ft.FontWeight.BOLD),
                    am_type, am_desc, am_burden, am_stage, am_user
                ]
                am_type.disabled = am_desc.disabled = am_burden.disabled = am_stage.disabled = am_user.disabled = False
                if am_sub_card: am_sub_card.visible = True
            else:
                btn_custom.style = None
                btn_premade.style = ft.ButtonStyle(bgcolor=ft.Colors.BLUE_700)
                am_panels.controls = [
                    ft.Text("Pre-Made Stacking", size=20, weight=ft.FontWeight.BOLD),
                    am_pre_body, am_pre_head, am_pre_breath
                ]
                am_type.disabled = am_desc.disabled = am_burden.disabled = am_stage.disabled = am_user.disabled = True
                if am_sub_card: am_sub_card.visible = False
            update_am_output()

        def reset_am(e):
            nonlocal am_selected_opts, am_selected_drawbacks, last_am_type
            am_selected_opts = set(am.STANDARD_SUBSYSTEMS.get("D", []))
            am_selected_drawbacks = {}
            last_am_type = "D"
            am_type.value = "D"
            am_desc.value = ""
            am_burden.value = ""
            am_stage.value = ""
            am_user.value = ""
            am_pre_body.value = am_pre_head.value = am_pre_breath.value = None
            update_am_output()
            switch_sub_tab("comms")

        btn_custom = ft.TextButton("Custom (System)", data="Custom", on_click=switch_am_mode, style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_700))
        btn_premade = ft.TextButton("Pre-Made (Items)", data="Premade", on_click=switch_am_mode)
        btn_reset = ft.TextButton("Reset System", on_click=reset_am, icon=ft.Icons.RESTART_ALT)
        
        # Attach events
        am_type.on_change = on_am_type_change
        am_desc.on_change = lambda _: update_am_output()
        am_burden.on_change = lambda _: update_am_output()
        am_stage.on_change = lambda _: update_am_output()
        am_user.on_change = lambda _: update_am_output()
        am_pre_body.on_change = lambda _: update_am_output()
        am_pre_head.on_change = lambda _: update_am_output()
        am_pre_breath.on_change = lambda _: update_am_output()

        # Initial data
        update_am_output() # Use this instead of on_am_type_change to ensure full refresh

        # Store cards for visibility toggling
        am_core_card = glass_card(
            ft.Column([
                ft.Row([btn_custom, btn_premade], spacing=10),
                ft.Divider(color=ft.Colors.WHITE10),
                am_panels,
                btn_reset
            ], spacing=10),
            title="Armor Config", color=ft.Colors.BLUE_400
        )
        
        am_sub_card = glass_card(
            ft.Column([
                ft.Row(sub_btns, spacing=5, scroll=ft.ScrollMode.AUTO),
                ft.Divider(color=ft.Colors.WHITE10),
                sub_tab_container
            ], spacing=10),
            title="Subsystems", color=ft.Colors.CYAN_400
        )

        return ft.Row([
            ft.Column([
                am_core_card,
                am_sub_card
            ], expand=2, spacing=20, scroll=ft.ScrollMode.AUTO),
            ft.Column([
                glass_card(
                    ft.Column([
                        am_res_model,
                        am_res_name,
                        ft.Divider(color=ft.Colors.WHITE10),
                        ft.Column([am_res_tl, am_res_cost, am_res_mass, am_res_qrebs], spacing=5),
                        ft.Divider(color=ft.Colors.WHITE10),
                        ft.Text("Protection", size=18, weight=ft.FontWeight.W_500),
                        am_res_pills,
                        ft.Divider(color=ft.Colors.WHITE10),
                        ft.Text("System Evaluation", size=18, weight=ft.FontWeight.W_500),
                        ft.Row([
                            ft.Column([ft.Text("Str (C1)", size=12, color=ft.Colors.GREY_400), am_res_str], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            ft.Column([ft.Text("Dex (C2)", size=12, color=ft.Colors.GREY_400), am_res_dex], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            ft.Column([ft.Text("End (C3)", size=12, color=ft.Colors.GREY_400), am_res_end], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                        ft.Row([ft.Text("Skill:", size=12, color=ft.Colors.GREY_400), am_res_skill], spacing=10),
                        ft.Divider(color=ft.Colors.WHITE10),
                        ft.Text("Equipment / Notes", size=18, weight=ft.FontWeight.W_500),
                        am_res_notes
                    ], spacing=10),
                    title="Armor Profile", color=ft.Colors.AMBER_400
                )
            ], expand=1, spacing=20)
        ], expand=True, spacing=20)

    def get_dice_view():
        # Core state for the dice roller
        history_column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=10)
        dm_spinner = NumericSpinner("DM (Modifier)", value=0, min_val=-20, max_val=20)
        n_dice_spinner = NumericSpinner("Dice Quantity", value=2, min_val=1, max_val=15)
        tn_input = ft.TextField(label="Target Number", width=120, height=50, text_align=ft.TextAlign.CENTER, keyboard_type=ft.KeyboardType.NUMBER)
        
        def add_to_history(result_text, color=ft.Colors.WHITE):
            history_column.controls.insert(0, ft.Text(result_text, size=16, color=color))
            if len(history_column.controls) > 20:
                history_column.controls.pop()
            page.update()

        def roll_dice_click(n_dice, label):
            total, rolls = dd.dice_detailed(n_dice)
            dm = dm_spinner.value
            final_total = total + dm
            
            # Spectacular Flags
            n_1s = rolls.count(1)
            n_6s = rolls.count(6)
            spec_succ = n_1s >= 3
            spec_fail = n_6s >= 3
            
            # Format history entry
            rolls_str = ", ".join(map(str, rolls))
            dm_str = f" {'+' if dm >= 0 else ''}{dm}" if dm != 0 else ""
            res_text = f"[{label}] [{rolls_str}]{dm_str} = {final_total}"
            
            # Target Number Logic
            status = ""
            color = ft.Colors.WHITE
            if tn_input.value:
                try:
                    tn = int(tn_input.value)
                    if final_total <= tn:
                        status = " - SUCCESS"
                        color = ft.Colors.GREEN_400
                    else:
                        status = " - FAILURE"
                        color = ft.Colors.RED_400
                    
                    if spec_succ and spec_fail:
                        status += " (SPECTACULAR INTERESTING!)"
                        color = ft.Colors.PURPLE_400
                    elif spec_succ:
                        status += " (SPECTACULAR SUCCESS!)"
                        color = ft.Colors.AMBER
                    elif spec_fail:
                        status += " (SPECTACULAR FAILURE!)"
                        color = ft.Colors.RED_700
                except:
                    pass
            else:
                # Default highlighting without TN
                if final_total >= 11 and n_dice == 2: color = ft.Colors.AMBER
                elif final_total <= 3 and n_dice == 2: color = ft.Colors.RED_400

            add_to_history(f"{res_text}{status}", color)

        def roll_flux_click(e):
            total, rolls = dd.flux_detailed()
            res_text = f"[Flux] [{rolls[0]}, {rolls[1]}] = {total}"
            add_to_history(res_text, ft.Colors.CYAN_200)

        # Build Buttons
        difficulties = [
            ("Easy", 1, ft.Colors.GREEN_400),
            ("Average", 2, ft.Colors.BLUE_400),
            ("Difficult", 3, ft.Colors.ORANGE_400),
            ("Formidable", 4, ft.Colors.RED_400),
            ("Staggering", 5, ft.Colors.PURPLE_400),
            ("Impossible", 6, ft.Colors.PINK_400),
        ]
        
        row1 = []
        row2 = []
        for i, (label, n, color) in enumerate(difficulties):
            btn = ft.FilledButton(
                content=ft.Column([
                    ft.Text(label, size=12, weight=ft.FontWeight.BOLD),
                    ft.Text(f"{n}D", size=10, italic=True)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                on_click=lambda e, n=n, l=label: roll_dice_click(n, l),
                style=ft.ButtonStyle(
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.with_opacity(0.1, color),
                    side=ft.BorderSide(1, ft.Colors.with_opacity(0.4, color)),
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
                width=135, height=60
            )
            if i < 3: row1.append(btn)
            else: row2.append(btn)

        flux_btn = ft.FilledButton(
            "FLUX", 
            on_click=roll_flux_click,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.CYAN_400),
                side=ft.BorderSide(1, ft.Colors.CYAN_700),
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            width=135, height=60
        )

        roll_n_btn = ft.FilledButton(
            "ROLL N",
            icon=ft.Icons.CASINO,
            on_click=lambda e: roll_dice_click(n_dice_spinner.value, f"{n_dice_spinner.value}D"),
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.AMBER_400),
                side=ft.BorderSide(1, ft.Colors.AMBER_700),
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            width=135, height=60
        )

        return ft.Column([
            glass_card(
                ft.Column([
                    ft.Text("Quick Rolls", size=18, weight=ft.FontWeight.W_500),
                    ft.Row(row1, spacing=10),
                    ft.Row(row2, spacing=10),
                    ft.Divider(height=10, color=ft.Colors.WHITE10),
                    ft.Text("Custom Roll & Modifier", size=18, weight=ft.FontWeight.W_500),
                    ft.Row([n_dice_spinner, roll_n_btn], spacing=20, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.Row([dm_spinner, tn_input], spacing=20, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.Row([flux_btn], spacing=20),
                ], spacing=15),
                title="Dice Roller",
                subtitle="Execute standard Traveller checks and flux rolls.",
                color=ft.Colors.AMBER_400
            ),
            glass_card(
                ft.Column([
                    ft.Row([
                        ft.Text("Roll History", size=18, weight=ft.FontWeight.W_500),
                        ft.IconButton(ft.Icons.DELETE_OUTLINE, on_click=lambda _: history_column.controls.clear() or page.update(), icon_size=20)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Divider(height=1, color=ft.Colors.WHITE10),
                    ft.Container(history_column, height=300)
                ], spacing=10),
                color=ft.Colors.GREY_400
            )
        ], expand=True, spacing=20, scroll=ft.ScrollMode.AUTO)

    def get_sysgen_view():
        # --- Subsector View Elements ---
        sub_grid = ft.Column(scroll=ft.ScrollMode.AUTO, height=400, spacing=5)
        
        def on_subsector_click(e):
            try:
                seed = int(sys_seed.value) if sys_seed.value else 0
                systems = ts.fun_subsector(seed)
                sub_grid.controls = []
                for s in systems:
                    sub_grid.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Text(s['coord'], weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER, width=50),
                                ft.Text(s['uwp'], width=100, selectable=True, size=13),
                                ft.Text(s['pbg'], width=40, color=ft.Colors.GREY_400, size=13),
                                ft.Text(s['bases'], width=30, color=ft.Colors.PURPLE_200, size=13),
                                ft.Text(s['ext'], width=130, color=ft.Colors.PURPLE_200, size=12),
                                ft.Text(s['trade'], size=11, color=ft.Colors.CYAN_200, expand=True)
                            ], spacing=5),
                            padding=10,
                            bgcolor=ft.Colors.WHITE10,
                            border_radius=5
                        )
                    )
                sub_grid.visible = True
            except Exception as ex:
                sub_grid.controls = [ft.Text(f"Error: {str(ex)}", color=ft.Colors.RED_400)]
            page.update()

        # Sub-tab views
        standalone_view = ft.Column([
            ft.FilledButton(
                "Generate System", 
                icon=ft.Icons.AUTO_AWESOME, 
                on_click=on_sys_gen_click,
                style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.PURPLE_700),
                height=50, width=250
            ),
            ft.Container(
                content=sys_result,
                padding=20,
                border_radius=15,
                bgcolor=ft.Colors.BLACK54,
                border=ft.Border.all(1, ft.Colors.PURPLE_900),
            )
        ], spacing=20, visible=True)

        mapping_view = ft.Column([
            ft.FilledButton(
                "Generate Subsector", 
                icon=ft.Icons.GRID_VIEW, 
                on_click=on_subsector_click,
                style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE_700),
                height=50, width=250
            ),
            sub_grid
        ], spacing=20, visible=False)

        def switch_gen_mode(e):
            mode = e.control.data
            standalone_view.visible = (mode == "single")
            mapping_view.visible = (mode == "mapping")
            for btn in mode_btns:
                btn.style = ft.ButtonStyle(bgcolor=ft.Colors.PURPLE_700 if btn.data == mode else None)
            page.update()

        mode_btns = [
            ft.TextButton("Standalone System", icon=ft.Icons.PUBLIC, data="single", on_click=switch_gen_mode, style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE_700)),
            ft.TextButton("Subsector Mapping", icon=ft.Icons.MAP, data="mapping", on_click=switch_gen_mode),
        ]

        return ft.Column([
            glass_card(
                ft.Column([
                    ft.Row([
                        sys_seed,
                        ft.IconButton(ft.Icons.REFRESH, on_click=on_random_seed_click, tooltip="Random Seed")
                    ], spacing=10),
                    ft.Row(mode_btns, spacing=10),
                    ft.Divider(height=10, color=ft.Colors.WHITE10),
                    standalone_view,
                    mapping_view
                ], spacing=20),
                title="Galaxy Engine",
                subtitle="Generate worlds and entire subsectors from static seeds.",
                color=ft.Colors.PURPLE_300
            )
        ], expand=True, spacing=20)

    # --- Main Navigation ---
    main_content = ft.Container(padding=30, expand=True)
    
    def navigate(e):
        index = e.control.selected_index
        if index == 0:
            main_content.content = get_dice_view()
        elif index == 1:
            main_content.content = get_sysgen_view()
        elif index == 2:
            main_content.content = get_buy_view()
        elif index == 3:
            main_content.content = get_sell_view()
        elif index == 4:
            main_content.content = get_travel_view()
        elif index == 5:
            main_content.content = get_qrebs_view()
        elif index == 6:
            main_content.content = get_gm_view()
        elif index == 7:
            main_content.content = get_am_view()
        page.update()

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        bgcolor="#0F1218",
        leading=ft.Container(
            content=ft.Icon(ft.Icons.AUTO_AWESOME_MOTION, color=ft.Colors.AMBER, size=35),
            padding=ft.Padding(0, 20, 0, 20)
        ),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.CASINO, selected_icon=ft.Icons.CASINO, label="Dice Roller"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.PUBLIC, selected_icon=ft.Icons.PUBLIC, label="System Gen"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SHOPPING_BAG, selected_icon=ft.Icons.SHOPPING_BAG, label="Trade: Buy"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SELL, selected_icon=ft.Icons.SELL, label="Trade: Sell"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.FLIGHT_TAKEOFF, selected_icon=ft.Icons.FLIGHT_TAKEOFF, label="Travel"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.QR_CODE_2_OUTLINED,
                selected_icon=ft.Icons.QR_CODE_2,
                label="QREBS Tool",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.HANDYMAN, selected_icon=ft.Icons.HANDYMAN, label="GunMaker"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SHIELD, selected_icon=ft.Icons.SHIELD, label="ArmourMaker"
            ),
        ],
        on_change=navigate,
    )

    # Initial view
    main_content.content = get_dice_view()
    
    page.add(
        ft.Row([
            rail,
            ft.VerticalDivider(width=1, color=ft.Colors.WHITE10),
            main_content
        ], expand=True, spacing=0)
    )
    page.update()

ft.run(main)

