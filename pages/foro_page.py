import flet as ft

def ForoPage(page: ft.Page):
    mensajes = ft.Column(scroll="always", expand=True)
    entrada = ft.TextField(label="Escribe tu pregunta o comentario", expand=True)

    def enviar_mensaje(e):
        if entrada.value.strip():
            mensajes.controls.append(ft.Text(f"👤 {entrada.value}"))
            entrada.value = ""
            page.update()

    return ft.View(
        "/foro",
        [
            ft.AppBar(title=ft.Text("Foro Académico"), bgcolor=ft.Colors.BLUE_300),
            mensajes,
            ft.Row([entrada, ft.IconButton(icon=ft.Icons.SEND, on_click=enviar_mensaje)]),
            ft.ElevatedButton("Regresar", on_click=lambda e: page.go("/home")),
        ],
    )
