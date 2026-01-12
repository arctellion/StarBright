import flet as ft
import travtools.qrebs as qrebs_gen
from views.components import glass_card, NumericSpinner, Styles

class QrebsView(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True, spacing=20, scroll=ft.ScrollMode.AUTO)
        self.app_page = page
        self.gen_output = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, height=400)
        self.gen_qty = NumericSpinner("Quantity", value=1, min_val=1, max_val=20)
        self.dec_input = ft.TextField(label="Enter QREBS Code", max_length=5, text_style=ft.TextStyle(letter_spacing=2), border_color=Styles.BORDER_COLOR)
        self.dec_output = ft.Column()
        self.build_ui()

    def build_ui(self):
        # Accordion UI using ExpansionTiles
        self.controls = [
            ft.ExpansionTile(
                title=ft.Text("QREBS Generator", size=18, weight=ft.FontWeight.W_500, color=Styles.PURPLE),
                controls=[
                    ft.Container(
                        content=ft.Column([
                            ft.Row([self.gen_qty, ft.FilledButton("Generate", icon=ft.Icons.STARS, on_click=self.on_generate_qrebs, style=ft.ButtonStyle(bgcolor=Styles.PURPLE))]),
                            ft.Divider(color=ft.Colors.WHITE10),
                            self.gen_output
                        ]),
                        padding=15
                    )
                ]
            ),
            ft.ExpansionTile(
                title=ft.Text("QREBS Decoder", size=18, weight=ft.FontWeight.W_500, color=Styles.TEAL),
                controls=[
                    ft.Container(
                        content=ft.Column([
                            ft.Row([self.dec_input, ft.FilledButton("Decode", icon=ft.Icons.TRANSLATE, on_click=self.on_decode_qrebs, style=ft.ButtonStyle(bgcolor=Styles.TEAL))]),
                            ft.Divider(color=ft.Colors.WHITE10),
                            self.dec_output
                        ]),
                        padding=15
                    )
                ]
            )
        ]

    def on_generate_qrebs(self, e):
        try:
            self.gen_output.controls.clear()
            for _ in range(self.gen_qty.value):
                res = qrebs_gen.generate_qrebs()
                self.gen_output.controls.append(ft.ExpansionTile(title=ft.Text(f"Code: {res['code']}", size=18, weight=ft.FontWeight.BOLD, color=Styles.CYAN), controls=[ft.Container(content=ft.Text(res['text'], size=14, color=ft.Colors.GREY_300), padding=15, bgcolor=ft.Colors.BLACK54, border_radius=10)]))
        except Exception as ex: self.gen_output.controls = [ft.Text(f"Error: {ex}", color=ft.Colors.RED)]
        try: self.update()
        except: pass

    def on_decode_qrebs(self, e):
        try:
            code = self.dec_input.value.upper()
            if len(code) != 5: self.dec_output.controls = [ft.Text("Enter 5-char code", color=ft.Colors.RED_400)]
            else:
                res = qrebs_gen.decode_qrebs(code)
                color = ft.Colors.GREEN_400 if res['valid'] else ft.Colors.RED_400
                self.dec_output.controls = [ft.Container(content=ft.Text(res['text'], size=16), padding=20, border=ft.Border.all(1, color), border_radius=10, bgcolor=ft.Colors.BLACK54)]
        except Exception as ex: self.dec_output.controls = [ft.Text(f"Error: {ex}", color=ft.Colors.RED)]
        try: self.update()
        except: pass
