import flet as ft

# --- Centralized Design System ---
class Styles:
    BG_COLOR = "#0B0E14"
    CARD_BG = "#161B22"
    GLASS_OPACITY = 0.1
    GLASS_BLUR = 0
    BORDER_OPACITY = 0.1
    BORDER_COLOR = ft.Colors.WHITE10
    
    # Accent Colors
    AMBER = ft.Colors.AMBER_400
    BLUE = ft.Colors.BLUE_400
    GREEN = ft.Colors.GREEN_400
    CYAN = ft.Colors.CYAN_400
    PURPLE = ft.Colors.PURPLE_400
    TEAL = ft.Colors.TEAL_400

def glass_card(content, title=None, subtitle=None, color=Styles.BLUE, expand=False, **kwargs):
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
            ft.Container(content, padding=ft.Padding(0, 10, 0, 0), expand=True if expand else False)
        ], spacing=15, expand=True if expand else False),
        padding=25,
        bgcolor=Styles.CARD_BG,
        border=ft.border.all(1, Styles.BORDER_COLOR),
        border_radius=15,
        expand=expand,
        shadow=None,
        **kwargs
    )

class NumericSpinner(ft.Row):
    def __init__(self, label, value=0, min_val=0, max_val=15, on_change=None):
        super().__init__(spacing=5, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        self.min_val = min_val
        self.max_val = max_val
        self.on_change_cb = on_change
        self.text_field = ft.TextField(
            value=str(value),
            label=label,
            width=100,
            text_size=14,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=Styles.BORDER_COLOR,
            focused_border_color=Styles.BLUE
        )
        self.text_field.on_change = self.validate
        self.btn_minus = ft.IconButton(ft.Icons.REMOVE_CIRCLE_OUTLINE, icon_size=20, icon_color=ft.Colors.GREY_400)
        self.btn_minus.on_click = self.minus_click
        
        self.btn_plus = ft.IconButton(ft.Icons.ADD_CIRCLE_OUTLINE, icon_size=20, icon_color=ft.Colors.GREY_400)
        self.btn_plus.on_click = self.plus_click
        
        self.controls = [
            self.btn_minus,
            self.text_field,
            self.btn_plus,
        ]

    def minus_click(self, e):
        curr = int(self.text_field.value)
        if curr > self.min_val:
            self.text_field.value = str(curr - 1)
            if self.on_change_cb: self.on_change_cb(e)
            self.update()

    def plus_click(self, e):
        curr = int(self.text_field.value)
        if curr < self.max_val:
            self.text_field.value = str(curr + 1)
            if self.on_change_cb: self.on_change_cb(e)
            self.update()

    def validate(self, e):
        try:
            val = int(self.text_field.value)
            if val < self.min_val: self.text_field.value = str(self.min_val)
            if val > self.max_val: self.text_field.value = str(self.max_val)
        except:
            self.text_field.value = str(self.min_val)
        if self.on_change_cb: self.on_change_cb(e)
            
    @property
    def value(self):
        try:
            return int(self.text_field.value)
        except:
            return self.min_val
    
    @value.setter
    def value(self, val):
        self.text_field.value = str(val)
        try: self.update()
        except: pass
