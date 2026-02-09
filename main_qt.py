"""
Main entry point for the StarBright application.
Initializes the PyQt6 application, sets up the main navigation menu,
and manages the view stack.
"""
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMenuBar, QPushButton

from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from views.qt_components import Styles

class StarBrightApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StarBright - Traveller Toolbox (PyQt6)")
        self.resize(1100, 800)
        self.setStyleSheet(Styles.MAIN_STYLE)
        
        # Central Widget & Stack
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)
        
        # Registry for views
        self.views = {}
        
        self.init_menu()
        self.show_initial_view()

    def init_menu(self):
        menubar = self.menuBar()
        
        # Galaxy Engine
        galaxy_menu = menubar.addMenu("Galaxy Engine")
        self.add_nav_action(galaxy_menu, "System", self.show_system)
        self.add_nav_action(galaxy_menu, "SubSector", self.show_subsector)
        self.add_nav_action(galaxy_menu, "Sector", self.show_sector)
        self.add_nav_action(galaxy_menu, "Traveller Map", self.show_traveller_map)
        
        # Trading
        trade_menu = menubar.addMenu("Trading")
        self.add_nav_action(trade_menu, "Buying", self.show_buy)
        self.add_nav_action(trade_menu, "Selling", self.show_sell)
        
        # Makers
        makers_menu = menubar.addMenu("Makers")
        self.add_nav_action(makers_menu, "Guns", self.show_guns)
        self.add_nav_action(makers_menu, "Armor", self.show_armor)
        self.add_nav_action(makers_menu, "Vehicles", self.show_vehicles)
        
        # Utilities
        utils_menu = menubar.addMenu("Utilities")
        self.add_nav_action(utils_menu, "Dice Roller", self.show_dice)
        self.add_nav_action(utils_menu, "Travel", self.show_travel)
        self.add_nav_action(utils_menu, "QREBS", self.show_qrebs)
        self.add_nav_action(utils_menu, "Name Generator", self.show_names)

        # Right-aligned Buttons
        corner_widget = QWidget()
        corner_layout = QHBoxLayout(corner_widget)
        corner_layout.setContentsMargins(0, 0, 0, 0)
        corner_layout.setSpacing(5)

        about_btn = QPushButton("About")
        about_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #42A5F5;
                font-weight: bold;
                padding: 5px 10px;
                border: none;
            }
            QPushButton:hover {
                background: #42A5F5;
                color: #0B0E14;
            }
        """)
        about_btn.clicked.connect(self.show_initial_view)

        exit_btn = QPushButton("Exit")
        exit_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #ff5555;
                font-weight: bold;
                padding: 5px 15px;
                border: none;
            }
            QPushButton:hover {
                background: #ff5555;
                color: white;
            }
        """)
        exit_btn.clicked.connect(self.close)
        
        corner_layout.addWidget(about_btn)
        corner_layout.addWidget(exit_btn)
        menubar.setCornerWidget(corner_widget, Qt.Corner.TopRightCorner)



    def add_nav_action(self, menu, label, callback, disabled=False):
        action = QAction(label, self)
        if callback:
            action.triggered.connect(callback)
        if disabled:
            action.setEnabled(False)
        menu.addAction(action)
        return action

    def switch_view(self, name, widget_class):
        if name not in self.views:
            # Lazy load view
            view = widget_class()
            self.views[name] = view
            self.stack.addWidget(view)
        
        self.stack.setCurrentWidget(self.views[name])

    # Navigation Callbacks
    def show_system(self):
        from views.galaxy_qt import SystemQtView
        self.switch_view("System", SystemQtView)

    def show_subsector(self):
        from views.galaxy_qt import SubsectorQtView
        self.switch_view("SubSector", SubsectorQtView)

    def show_sector(self):
        from views.galaxy_qt import SectorQtView
        self.switch_view("Sector", SectorQtView)

    def show_traveller_map(self):
        from views.galaxy_qt import TravellerMapQtView
        self.switch_view("Traveller Map", TravellerMapQtView)

    def show_buy(self):
        from views.trade_qt import BuyQtView
        self.switch_view("Buying", BuyQtView)

    def show_sell(self):
        from views.trade_qt import SellQtView
        self.switch_view("Selling", SellQtView)

    def show_guns(self):
        from views.gun_qt import GunQtView
        self.switch_view("Guns", GunQtView)

    def show_armor(self):
        from views.armour_qt import ArmourQtView
        self.switch_view("Armor", ArmourQtView)

    def show_vehicles(self):
        from views.vehicle_qt import VehicleQtView
        self.switch_view("Vehicles", VehicleQtView)

    def show_dice(self):
        from views.dice_qt import DiceQtView
        self.switch_view("Dice Roller", DiceQtView)

    def show_travel(self):
        from views.utils_qt import TravelQtView
        self.switch_view("Travel", TravelQtView)

    def show_qrebs(self):
        from views.utils_qt import QrebsQtView
        self.switch_view("QREBS", QrebsQtView)

    def show_names(self):
        from views.names_qt import NamesQtView
        self.switch_view("Name Generator", NamesQtView)

    def show_initial_view(self):
        from views.utils_qt import WelcomeQtView
        self.switch_view("Welcome", WelcomeQtView)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StarBrightApp()
    window.show()
    sys.exit(app.exec())
