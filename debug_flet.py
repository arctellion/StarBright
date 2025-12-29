import flet as ft

def main(page: ft.Page):
    page.bgcolor = ft.Colors.RED
    page.add(ft.Text("Flet is working!", size=50, color=ft.Colors.WHITE))
    page.update()

ft.run(main)
