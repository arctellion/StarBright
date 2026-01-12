import flet as ft
import re
import travtools.commerce as cm
from views.components import glass_card, NumericSpinner, Styles

class TradeView(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True, spacing=20, scroll=ft.ScrollMode.AUTO)
        self.app_page = page
        self.uwp_pat = re.compile('[ABCDEXFGHY][0-9A-F][0-9A-F][0-9A][0-9A-F][0-9A-F][0-9A-J]-[0-9A-J]')
        
        # --- Buy UI Elements ---
        self.buy_uwp = ft.TextField(label="UWP (e.g., A110877-E)", border_color=Styles.BLUE, expand=True)
        self.buy_steward = NumericSpinner("Steward", value=0)
        self.buy_admin = NumericSpinner("Admin", value=0)
        self.buy_street = NumericSpinner("Streetwise", value=0)
        self.buy_liaison = NumericSpinner("Liaison", value=0)
        self.buy_days = NumericSpinner("Days", value=7, min_val=1, max_val=14)
        self.buy_result = ft.Text(selectable=True)
        
        # --- Sell UI Elements ---
        self.sell_cargo = ft.TextField(label="Cargo ID (e.g., B - Ri Cr5,100)", border_color=Styles.GREEN)
        self.sell_uwp = ft.TextField(label="Destination UWP", border_color=Styles.GREEN)
        self.sell_broker = ft.Dropdown(label="Broker Skill", options=[ft.DropdownOption(str(i)) for i in range(16)], value="0")
        self.sell_trade_roll = ft.Dropdown(label="Trade pre-roll (optional)", options=[ft.DropdownOption(str(i)) for i in range(7)], value="0")
        self.sell_result = ft.Text(selectable=True)

        self.build_ui()

    def build_ui(self):
        # Accordion-style layout using ExpansionTiles
        self.controls = [
            ft.ExpansionTile(
                title=ft.Text("Speculative Trade: Buy", size=18, weight=ft.FontWeight.W_500, color=Styles.BLUE),
                controls=[self.get_buy_view()]
            ),
            ft.ExpansionTile(
                title=ft.Text("Speculative Trade: Sell", size=18, weight=ft.FontWeight.W_500, color=Styles.GREEN),
                controls=[self.get_sell_view()]
            )
        ]
        # Flet 0.8.0 initially_expanded fix (expand first by default if possible, or just accept collapsed)
        # Note: 0.8.0 doesn't have an easy "expand" method on ExpansionTile either without page access later.

    def on_buy_click(self, e):
        self.buy_result.value = ""
        uwp = self.buy_uwp.value.upper()
        if not uwp: self.buy_result.value = "Error: No UWP Provided."
        elif len(uwp) != 9: self.buy_result.value = "Error: Incorrect length UWP (should be 9 chars)."
        elif not self.uwp_pat.match(uwp): self.buy_result.value = "Error: Incorrect UWP pattern."
        else:
            try:
                skills = {'Steward': self.buy_steward.value, 'Admin': self.buy_admin.value, 'Streetwise': self.buy_street.value, 'Liaison': self.buy_liaison.value}
                trade_data = cm.trade_gds(uwp, skills, self.buy_days.value)
                self.buy_result.value = trade_data if trade_data else "No goods found / Error in calculation."
            except Exception as ex: self.buy_result.value = f"Error: {str(ex)}"
        try: self.update()
        except: pass

    def on_sell_click(self, e):
        self.sell_result.value = ""
        uwp = self.sell_uwp.value.upper(); cargo = self.sell_cargo.value
        if not cargo: self.sell_result.value = "Error: No Cargo Code entered."
        elif len(uwp) != 9: self.sell_result.value = "Error: Incorrect length UWP."
        elif not self.uwp_pat.match(uwp): self.sell_result.value = "Error: Incorrect UWP Pattern."
        else:
            try:
                trd = int(self.sell_trade_roll.value) if self.sell_trade_roll.value else 0
                broker = int(self.sell_broker.value)
                value = cm.sell_price(cargo, uwp, broker, trd)
                if value > 0: self.sell_result.value = f"Sell Price: Cr{value:,}"
                else: self.sell_result.value = "No value found / Error in calculation."
            except Exception as ex: self.sell_result.value = f"Error: {str(ex)}"
        try: self.update()
        except: pass

    def get_buy_view(self):
        btn_generate = ft.FilledButton("Generate Goods", icon=ft.Icons.SEARCH, height=50, width=250, on_click=self.on_buy_click, style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_700))
        return ft.Container(
            content=ft.Column([
                glass_card(ft.Column([ft.Row([self.buy_uwp, self.buy_days], spacing=20), ft.Text("Character Skills", size=16, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE70), ft.Row([self.buy_steward, self.buy_admin, self.buy_street, self.buy_liaison], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), btn_generate], spacing=20), color=Styles.BLUE),
                ft.Container(content=self.buy_result, padding=20, border_radius=15, bgcolor=ft.Colors.BLACK54, border=ft.Border.all(1, ft.Colors.BLUE_900), margin=ft.Margin.only(top=10))
            ], spacing=20),
            padding=10
        )

    def get_sell_view(self):
        btn_calculate = ft.FilledButton("Calculate Sale Price", icon=ft.Icons.ATTACH_MONEY, height=50, width=250, on_click=self.on_sell_click, style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_700))
        return ft.Container(
            content=ft.Column([
                glass_card(ft.Column([self.sell_cargo, self.sell_uwp, ft.Row([self.sell_broker, self.sell_trade_roll], spacing=10), btn_calculate], spacing=20), color=Styles.GREEN),
                ft.Container(content=self.sell_result, padding=20, border_radius=15, bgcolor=ft.Colors.BLACK54, border=ft.Border.all(1, ft.Colors.GREEN_900), margin=ft.Margin.only(top=10))
            ], spacing=20),
            padding=10
        )
