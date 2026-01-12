import flet as ft
from travtools.travel import calculate_travel_time
from views.components import glass_card, Styles

class TravelView(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True, spacing=20)
        self.app_page = page
        
        # --- Travel Time UI Elements ---
        self.travel_adia = ft.TextField(label="Departure / Arrival Diameters", value="100", keyboard_type=ft.KeyboardType.NUMBER)
        self.travel_pdia = ft.TextField(label="Planet Diameter (km)", value="5000", keyboard_type=ft.KeyboardType.NUMBER)
        self.travel_spd = ft.TextField(label="Speed of Ship (G)", value="1", keyboard_type=ft.KeyboardType.NUMBER)
        self.travel_result = ft.Text(size=16, weight=ft.FontWeight.W_500)

        self.btn_calculate = ft.FilledButton("Calculate Time", icon=ft.Icons.TIMER, height=50, width=250, style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE_700))
        self.btn_calculate.on_click = self.on_travel_click

        self.controls = [self.get_travel_view()]

    def on_travel_click(self, e):
        try:
            a_dia = float(self.travel_adia.value or 0)
            p_dia = float(self.travel_pdia.value or 0)
            s_spd = float(self.travel_spd.value or 0)
            hr, mins = calculate_travel_time(a_dia, p_dia, s_spd)
            if hr is not None:
                self.travel_result.value = f"Estimated travel time: {hr} hours and {mins} minutes"
                self.travel_result.color = ft.Colors.GREEN_400
            else:
                self.travel_result.value = "Error: Invalid calculation parameters."
                self.travel_result.color = ft.Colors.RED_400
        except Exception as ex:
            self.travel_result.value = f"Error: {str(ex)}"
            self.travel_result.color = ft.Colors.RED_400
        try: self.update()
        except: pass
        try: self.app_page.update()
        except: pass

    def get_travel_view(self):
        return ft.Column([
            glass_card(ft.Column([self.travel_adia, self.travel_pdia, self.travel_spd, self.btn_calculate], spacing=20), title="Travel Time", color=ft.Colors.ORANGE_300),
            ft.Container(content=self.travel_result, padding=20, border_radius=15, bgcolor=ft.Colors.BLACK54, border=ft.Border.all(1, ft.Colors.ORANGE_900), margin=ft.Margin.only(top=10))
        ], expand=True, spacing=20, scroll=ft.ScrollMode.AUTO)
