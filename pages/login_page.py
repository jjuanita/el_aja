import flet as ft
from firebase_init import db
from theme_config import PRIMARY_COLOR, ACCENT_COLOR, BACKGROUND_COLOR, TITLE_STYLE, SUBTITLE_STYLE, LABEL_STYLE

def LoginPage(page: ft.Page):
    page.title = "EL AJA - Inicio de sesión"
    page.bgcolor = BACKGROUND_COLOR

    email_field = ft.TextField(
        label="Correo institucional",
        width=300,
        border_color=PRIMARY_COLOR,
        color=ft.Colors.BLACK,
        label_style=LABEL_STYLE
    )

    password_field = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=300,
        border_color=PRIMARY_COLOR,
        color=ft.Colors.BLACK,
        label_style=LABEL_STYLE
    )

    error_text = ft.Text("", color=ft.Colors.RED_600)

    def login(e):
        if not email_field.value.endswith("@utsjr.edu.mx"):
            error_text.value = "❌ Usa un correo institucional."
            page.update()
            return

        usuarios = db.collection("usuarios").where("correo", "==", email_field.value).stream()
        encontrado = False

        for u in usuarios:
            data = u.to_dict()
            if data["contraseña"] == password_field.value:
                encontrado = True
                page.session.set("usuario", email_field.value)
                page.go("/home")
                break

        if not encontrado:
            error_text.value = "❌ Credenciales incorrectas o usuario no registrado."
            page.update()

    return ft.View(
        "/",
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Image(src="assets/logo.png", width=160, height=160),
                        ft.Text("EL AJA", style=TITLE_STYLE),
                        ft.Text("Espacio de Logística Académica y Asesoría", style=SUBTITLE_STYLE),
                        ft.Divider(height=10, color=PRIMARY_COLOR),
                        email_field,
                        password_field,
                        ft.ElevatedButton(
                            "Iniciar sesión",
                            bgcolor=PRIMARY_COLOR,
                            color=ft.Colors.WHITE,
                            on_click=login,
                            width=200,
                        ),
                        ft.TextButton(
                            "Registrarme",
                            on_click=lambda e: page.go("/register"),
                            style=ft.ButtonStyle(color=ACCENT_COLOR),
                        ),
                        error_text,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=15,
                ),
                padding=30,
                margin=50,
                border_radius=20,
                bgcolor=ft.Colors.WHITE,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.BLUE_GREY_200,
                    offset=ft.Offset(0, 4),
                ),
                width=400,
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
    )
