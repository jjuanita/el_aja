import flet as ft

def HomePage(page: ft.Page):
    def navigate(e):
        page.go(e.control.data)

    return ft.View(
        "/home",
        controls=[
            ft.Text("Menú Principal - EL AJA", size=22, weight="bold"),
            ft.Text("Selecciona un módulo para comenzar:"),
            ft.Column(
                [
                    ft.ElevatedButton("Foro Académico", data="/foro", on_click=navigate),
                    ft.ElevatedButton("Chatbot Interactivo", data="/chatbot", on_click=navigate),
                    ft.ElevatedButton("Gestión de Talleres", data="/talleres", on_click=navigate),
                    ft.ElevatedButton("Cerrar sesión", data="/", on_click=navigate),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
    )
