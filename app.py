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
        "QREBS": QrebsView
    }
    
    # Cache for instantiated views
    instantiated_views = {}

    # Main content container
    main_container = ft.Container(expand=True, padding=20)
    
    def on_nav_change(e):
        index = int(e.control.selected_index)
        label = e.control.destinations[index].label
        
        # Lazy Loading Logic
        if label not in instantiated_views:
            view_class = view_classes[label]
            view_instance = view_class(page)
            instantiated_views[label] = view_instance
        
        # Swap content
        main_container.content = instantiated_views[label]
        page.update()

    # --- Sidebar Navigation ---
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        bgcolor=Styles.CARD_BG,
        indicator_color=Styles.BLUE,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.MONETIZATION_ON_OUTLINED, selected_icon=ft.Icons.MONETIZATION_ON, label="Trade"),
            ft.NavigationRailDestination(icon=ft.Icons.FLIGHT_TAKEOFF_OUTLINED, selected_icon=ft.Icons.FLIGHT_TAKEOFF, label="Travel"),
            ft.NavigationRailDestination(icon=ft.Icons.LANGUAGE_OUTLINED, selected_icon=ft.Icons.LANGUAGE, label="Systems"),
            ft.NavigationRailDestination(icon=ft.Icons.CONSTRUCTION_OUTLINED, selected_icon=ft.Icons.CONSTRUCTION, label="Guns"),
            ft.NavigationRailDestination(icon=ft.Icons.SHIELD_OUTLINED, selected_icon=ft.Icons.SHIELD, label="Armor"),
            ft.NavigationRailDestination(icon=ft.Icons.QR_CODE_OUTLINED, selected_icon=ft.Icons.QR_CODE, label="QREBS"),
        ],
        on_change=on_nav_change
    )

    # Load initial view (Trade)
    initial_view = TradeView(page)
    instantiated_views["Trade"] = initial_view
    main_container.content = initial_view

    # --- Main Layout ---
    page.add(
        ft.Row([
            rail,
            ft.VerticalDivider(width=1, color=ft.Colors.WHITE10),
            main_container
        ], expand=True)
    )

if __name__ == "__main__":
    try:
        ft.run(main)
    except (ConnectionResetError, KeyboardInterrupt, EOFError):
        pass
