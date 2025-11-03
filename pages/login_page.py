import flet as ft
from firebase_init import db

def LoginPage(page: ft.Page):
    email_field = ft.TextField(label="Correo institucional", width=300)
    password_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    error_text = ft.Text("", color=ft.Colors.RED_600)

    def login(e):
        if not email_field.value.endswith("@utsjr.edu.mx"):
            error_text.value = "❌ Usa un correo institucional (@utsjr.edu.mx)."
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
            ft.Column(
                [
                    ft.Image(src="assets/logo.png", width=160, height=160),
                    ft.Text("EL AJA", size=28, weight="bold"),
                    ft.Text("Espacio de Logística Académica y Asesoría", italic=True),
                    email_field,
                    password_field,
                    ft.ElevatedButton("Iniciar sesión", on_click=login),
                    ft.TextButton("Registrarme", on_click=lambda e: page.go("/register")),
                    error_text,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=15,
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
    )
