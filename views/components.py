import flet as ft

def glass_card(content, title=None, subtitle=None, color=ft.Colors.BLUE_400):
    """
    Creates a 'Glass' themed card container.
    """
    header_controls = []
    if title:
        header_controls.append(ft.Text(title, size=24, weight=ft.FontWeight.BOLD, color=color))
    if subtitle:
        header_controls.append(ft.Text(subtitle, size=14, color=ft.Colors.GREY_400))
        
    return ft.Container(
        content=ft.Column([
            ft.Column(header_controls, spacing=0) if header_controls else ft.Container(),
            ft.Container(content, padding=ft.Padding(0, 10, 0, 0))
        ], spacing=15),
        padding=25,
        bgcolor="#161B22",
        border=ft.border.all(1, ft.Colors.WHITE10),
        border_radius=15,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
        )
    )
