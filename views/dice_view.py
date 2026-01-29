import flet as ft
import travtools.dice as dd
from views.components import Styles, glass_card

class DiceView(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True, spacing=20, scroll=ft.ScrollMode.AUTO)
        self.app_page = page
        self.history = []
        
        # UI Elements
        self.result_text = ft.Text("Roll for Initiative", size=48, weight=ft.FontWeight.W_900, color=Styles.AMBER)
        self.detail_text = ft.Text("", size=18, color=ft.Colors.GREY_400)
        self.history_list = ft.ListView(expand=True, spacing=10, padding=10)
        self.custom_input = ft.TextField(
            label="Custom Roll (e.g., 2d6+3)", 
            value="2d6", 
            expand=True, 
            border_color=Styles.BORDER_COLOR,
            on_submit=self.on_custom_roll
        )
        
        self.build_ui()

    def build_ui(self):
        # Quick Roll Buttons
        quick_rolls = [
            ("Easy", 1, Styles.BLUE),
            ("Average", 2, Styles.GREEN),
            ("Difficult", 3, Styles.AMBER),
            ("Formidable", 4, Styles.PURPLE),
            ("Staggering", 5, Styles.CYAN),
            ("Impossible", 6, Styles.TEAL),
        ]
        
        buttons = []
        for label, n, color in quick_rolls:
            buttons.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(label, size=12, weight=ft.FontWeight.BOLD),
                        ft.Text(f"{n}d6", size=10, color=ft.Colors.GREY_400)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                    padding=10,
                    bgcolor=Styles.CARD_BG,
                    border=ft.border.all(1, Styles.BORDER_COLOR),
                    border_radius=8,
                    on_click=lambda e, n=n: self.roll_dice(n),
                    ink=True,
                    width=90
                )
            )
            
        # Flux Button
        buttons.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("Flux", size=12, weight=ft.FontWeight.BOLD),
                    ft.Text("2d6-7", size=10, color=ft.Colors.GREY_400)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                padding=10,
                bgcolor=Styles.CARD_BG,
                border=ft.border.all(1, Styles.BORDER_COLOR),
                border_radius=8,
                on_click=lambda e: self.roll_flux(),
                ink=True,
                width=90
            )
        )

        self.controls = [
            glass_card(
                content=ft.Column([
                    ft.Row(buttons, wrap=True, alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    ft.Divider(color=ft.Colors.WHITE10),
                    ft.Row([
                        self.custom_input,
                        ft.IconButton(ft.Icons.CASINO, on_click=self.on_custom_roll, icon_color=Styles.AMBER, icon_size=32)
                    ], spacing=10)
                ]),
                title="Dice Roller",
                subtitle="Quick options and custom rolls"
            ),
            ft.Row([
                glass_card(
                    content=ft.Column([
                        self.result_text,
                        self.detail_text
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER),
                    expand=True,
                    height=200
                ),
                glass_card(
                    content=self.history_list,
                    title="History",
                    expand=True,
                    height=200
                )
            ], expand=True, spacing=20)
        ]

    def roll_dice(self, n):
        total, rolls = dd.dice_detailed(n)
        self.update_display(f"{n}d6", total, rolls)

    def roll_flux(self):
        # User specified Flux (2d6-7) - though standard Traveller flux is 1d6-1d6 (-5 to +5)
        # 2d6-7 also gives -5 to +5.
        total = dd.dice(2) - 7
        self.update_display("Flux (2d6-7)", total, "2d6-7")

    def on_custom_roll(self, e):
        try:
            total, rolls, mod = dd.roll_string(self.custom_input.value)
            self.update_display(self.custom_input.value, total, f"{rolls} + {mod}" if mod else f"{rolls}")
        except Exception as ex:
            self.result_text.value = "Error"
            self.detail_text.value = str(ex)
            self.update()

    def update_display(self, label, total, details):
        self.result_text.value = str(total)
        self.detail_text.value = f"Rolled {label}: {details}"
        
        # Add to history
        self.history.insert(0, f"{label}: {total} ({details})")
        if len(self.history) > 20:
            self.history.pop()
            
        self.history_list.controls = [ft.Text(h, size=14) for h in self.history]
        
        self.update()
