import flet as ft
import travtools.system as ts
import random
from views.components import glass_card, Styles

class SystemView(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True, spacing=20, scroll=ft.ScrollMode.AUTO)
        self.app_page = page
        
        # --- Single System UI ---
        self.sys_seed = ft.TextField(label="System Seed", value="12345", keyboard_type=ft.KeyboardType.NUMBER, expand=True, border_color=Styles.BORDER_COLOR)
        self.sys_result = ft.Column(spacing=10)

        # --- Subsector UI ---
        self.sub_seed = ft.TextField(label="Subsector Seed", value="67890", keyboard_type=ft.KeyboardType.NUMBER, expand=True, border_color=Styles.BORDER_COLOR)
        self.sub_density = ft.Slider(min=0.1, max=1.0, value=0.5, divisions=9, label="{value}")
        self.sub_result = ft.Column(spacing=5, scroll=ft.ScrollMode.AUTO, height=400)

        self.build_ui()

    def build_ui(self):
        # Accordion-style layout using ExpansionTiles
        self.controls = [
            ft.ExpansionTile(
                title=ft.Text("System Generator (Single)", size=18, weight=ft.FontWeight.W_500, color=Styles.AMBER),
                controls=[
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                self.sys_seed, 
                                ft.FilledButton("Random", icon=ft.Icons.CASINO, on_click=self.on_random_seed_click, style=ft.ButtonStyle(bgcolor=Styles.BLUE)), 
                                ft.FilledButton("Generate", icon=ft.Icons.BRUSH, on_click=self.on_sys_gen_click, style=ft.ButtonStyle(bgcolor=Styles.AMBER))
                            ], spacing=10),
                            ft.Divider(color=ft.Colors.WHITE10),
                            self.sys_result
                        ]),
                        padding=15
                    )
                ]
            ),
            ft.ExpansionTile(
                title=ft.Text("Subsector Generator (8x10 Grid)", size=18, weight=ft.FontWeight.W_500, color=Styles.AMBER),
                controls=[
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                self.sub_seed, 
                                ft.Text("Density:"), 
                                self.sub_density, 
                                ft.FilledButton("Generate", icon=ft.Icons.GRID_VIEW, on_click=self.on_subsector_gen_click, style=ft.ButtonStyle(bgcolor=Styles.AMBER))
                            ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                            ft.Divider(color=ft.Colors.WHITE10),
                            self.sub_result
                        ]),
                        padding=15
                    )
                ]
            )
        ]

    def on_random_seed_click(self, e):
        self.sys_seed.value = str(random.randint(1000, 999999))
        try: self.update()
        except: pass

    def on_sys_gen_click(self, e):
        try:
            seed = int(self.sys_seed.value) if self.sys_seed.value else 0
            uwp = ts.fun_uwp(seed); pbg = ts.fun_pbg(uwp); bases = ts.fun_bases(uwp); trade = ts.fun_trade(uwp); ext = ts.fun_ext(uwp, pbg, bases, trade)
            self.sys_result.controls = [ft.Text(f"UWP: {uwp}", size=24, weight=ft.FontWeight.BOLD, color=Styles.AMBER), ft.Text(f"PBG: {pbg}", size=18), ft.Text(f"Bases: {bases if bases else 'None'}", size=18), ft.Text(f"Trade Codes: {trade}", size=18, color=Styles.CYAN), ft.Text(f"Extensions: {ext}", size=20, color=Styles.PURPLE)]
        except Exception as ex: 
            self.sys_result.controls = [ft.Text(f"Error: {ex}", color=ft.Colors.RED_400)]
        try: self.update()
        except: pass

    def on_subsector_gen_click(self, e):
        try:
            systems = ts.fun_subsector(int(self.sub_seed.value or 0), self.sub_density.value)
            self.sub_result.controls = []
            if not systems: self.sub_result.controls.append(ft.Text("Empty subsector", color=ft.Colors.RED_400))
            else:
                for s in systems: self.sub_result.controls.append(ft.Container(content=ft.Row([ft.Text(s['coord'], weight=ft.FontWeight.BOLD, width=50), ft.Text(s['uwp'], color=Styles.AMBER, width=120), ft.Text(s['trade'], color=Styles.CYAN, size=12, expand=True)]), padding=5, border=ft.Border(bottom=ft.BorderSide(1, ft.Colors.WHITE10))))
        except Exception as ex: 
            self.sub_result.controls = [ft.Text(f"Error: {ex}", color=ft.Colors.RED_400)]
        try: self.update()
        except: pass
