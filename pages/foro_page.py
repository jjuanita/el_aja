import flet as ft

def ForoPage(page: ft.Page):
    page.title = "Foro Académico - EL AJA"

    mensajes = ft.Column(scroll="always", expand=True)
    entrada = ft.TextField(
        label="Escribe tu pregunta o comentario",
        expand=True,
        border_color=ft.Colors.BLUE_300,
        focused_border_color=ft.Colors.BLUE_600,
        cursor_color=ft.Colors.BLUE_600,
        on_submit=None,   # <-- Se rellena después
    )

    def enviar_mensaje(e):
        if entrada.value.strip():
            mensajes.controls.append(
                ft.Text(
                    f"👤 Tú: {entrada.value}",
                    weight="bold",
                    color=ft.Colors.BLUE_600,
                )
            )
            mensajes.controls.append(
                ft.Text(
                    "📢 Tu mensaje ha sido publicado correctamente.",
                    color=ft.Colors.BLUE_300,
                    italic=True,
                )
            )
            entrada.value = ""
            page.update()
        else:
            # ✅ Mostrar alerta si está vacío
            page.snack_bar = ft.SnackBar(
                ft.Text("⚠️ El mensaje no puede estar vacío"),
                bgcolor=ft.Colors.RED_200,
                open=True
            )
            page.update()

    # ✅ Asignar ahora que la función ya existe
    entrada.on_submit = enviar_mensaje

    return ft.View(
        "/foro",
        [
            ft.AppBar(
                title=ft.Text("Foro Académico"),
                bgcolor=ft.Colors.BLUE_300,
                color=ft.Colors.WHITE,
            ),
            ft.Container(
                content=mensajes,
                padding=10,
                bgcolor=ft.Colors.BLUE_50,
                border_radius=10,
                expand=True,
            ),
            ft.Row(
                [entrada, ft.IconButton(icon=ft.Icons.SEND, on_click=enviar_mensaje)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.ElevatedButton(
                "Regresar",
                on_click=lambda e: page.go("/home"),
                bgcolor=ft.Colors.BLUE_600,
                color=ft.Colors.WHITE,
            ),
        ],
        scroll="adaptive",
    )