import flet as ft
import asyncio
import sys

# Mitigation for Windows ConnectionResetError on exit
if sys.platform == 'win32':
    import logging
    logging.getLogger("asyncio").setLevel(logging.CRITICAL)
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
from views.trade import TradeView
from views.travel_view import TravelView
from views.system_view import SystemView
from views.gun_view import GunView
from views.armour_view import ArmourView
from views.qrebs_view import QrebsView
from views.dice_view import DiceView
from views.components import Styles

def main(page: ft.Page):
    page.title = "StarBright - Traveller Toolbox"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1200
    page.window_height = 900
    page.bgcolor = "#050505"
    
    # View Registry for Lazy Loading
    view_classes = {
        "Trade": TradeView,
        "Travel": TravelView,
        "Systems": SystemView,
        "Guns": GunView,
        "Armor": ArmourView,
        "QREBS": QrebsView,
        "Dice Roller": DiceView
    }
    
    # Cache for instantiated views
    instantiated_views = {}

    # Main content container
    main_container = ft.Container(expand=True, padding=20)
    
    def set_view(label):
        if label not in instantiated_views:
            view_class = view_classes[label]
            view_instance = view_class(page)
            instantiated_views[label] = view_instance
        
        main_container.content = instantiated_views[label]
        page.update()

    def nav_item(label, icon, disabled=False):
        color = ft.Colors.GREY_600 if disabled else ft.Colors.WHITE70
        
        def on_click(_):
            if not disabled:
                mapping = {"System": "Systems"}
                target = mapping.get(label, label)
                set_view(target)

        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=18, color=color),
                ft.Text(label, size=14, color=color, weight=ft.FontWeight.W_500)
            ], spacing=10),
            padding=ft.Padding(20, 10, 0, 10),
            on_click=on_click,
            ink=not disabled,
            border_radius=8
        )

    sidebar = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text("STARBRIGHT", size=24, weight=ft.FontWeight.W_900, color=Styles.AMBER, italic=True),
                padding=20,
                alignment=ft.Alignment(0, 0)
            ),
            ft.ExpansionTile(
                title=ft.Text("Galaxy Engine", size=14, weight=ft.FontWeight.BOLD),
                expanded=True,
                controls=[
                    nav_item("System", ft.Icons.LANGUAGE), 
                    nav_item("SubSector", ft.Icons.GRID_VIEW, disabled=True),
                    nav_item("Sector", ft.Icons.MAP, disabled=True),
                ]
            ),
            ft.ExpansionTile(
                title=ft.Text("Trading", size=14, weight=ft.FontWeight.BOLD),
                controls=[
                    nav_item("Trade", ft.Icons.MONETIZATION_ON),
                    nav_item("Buying", ft.Icons.SHOPPING_CART, disabled=True),
                    nav_item("Selling", ft.Icons.SELL, disabled=True),
                ]
            ),
            ft.ExpansionTile(
                title=ft.Text("Makers", size=14, weight=ft.FontWeight.BOLD),
                controls=[
                    nav_item("Guns", ft.Icons.CONSTRUCTION),
                    nav_item("Armor", ft.Icons.SHIELD),
                ]
            ),
            ft.ExpansionTile(
                title=ft.Text("Utilities", size=14, weight=ft.FontWeight.BOLD),
                controls=[
                    nav_item("Dice Roller", ft.Icons.CASINO),
                    nav_item("Travel", ft.Icons.FLIGHT_TAKEOFF),
                    nav_item("QREBS", ft.Icons.QR_CODE),
                ]
            ),
        ], scroll=ft.ScrollMode.AUTO),
        width=250,
        bgcolor=Styles.CARD_BG,
        padding=10
    )

    # Load initial view (Trade)
    initial_view = TradeView(page)
    instantiated_views["Trade"] = initial_view
    main_container.content = initial_view

    # --- Main Layout ---
    page.add(
        ft.Row([
            sidebar,
            ft.VerticalDivider(width=1, color=ft.Colors.WHITE10),
            main_container
        ], expand=True)
    )

if __name__ == "__main__":
    try:
        ft.run(main)
    except (ConnectionResetError, KeyboardInterrupt, EOFError):
        pass
