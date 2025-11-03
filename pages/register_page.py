import flet as ft
from firebase_init import db

def RegisterPage(page: ft.Page):
    page.title = "Registro de usuario - EL AJA"

    nombre = ft.TextField(label="Nombre completo", width=300)
    correo = ft.TextField(label="Correo institucional", width=300)
    contraseña = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    confirmar = ft.TextField(label="Confirmar contraseña", password=True, can_reveal_password=True, width=300)
    mensaje = ft.Text("", color=ft.Colors.RED_600)

    def registrar(e):
        # Validar dominio institucional
        if not correo.value.endswith("@utsjr.edu.mx"):
            mensaje.value = "❌ Solo se permiten correos institucionales (@utsjr.edu.mx)."
        elif contraseña.value != confirmar.value:
            mensaje.value = "❌ Las contraseñas no coinciden."
        elif not nombre.value or not correo.value or not contraseña.value:
            mensaje.value = "⚠️ Completa todos los campos."
        else:
            # Guardar usuario en Firebase
            nuevo_usuario = {
                "nombre": nombre.value,
                "correo": correo.value,
                "contraseña": contraseña.value  # puedes usar hash más adelante
            }

            # Verificar si ya existe
            usuarios = db.collection("usuarios").where("correo", "==", correo.value).stream()
            if any(u for u in usuarios):
                mensaje.value = "⚠️ Este correo ya está registrado."
            else:
                db.collection("usuarios").add(nuevo_usuario)
                mensaje.value = "✅ Registro exitoso. Ya puedes iniciar sesión."
                mensaje.color = ft.Colors.GREEN_600

        page.update()

    return ft.View(
        "/register",
        [
            ft.AppBar(title=ft.Text("Registro de usuario"), bgcolor=ft.Colors.BLUE_300),
            ft.Column(
                [
                    ft.Text("Crear cuenta EL AJA", size=24, weight="bold"),
                    nombre,
                    correo,
                    contraseña,
                    confirmar,
                    ft.ElevatedButton("Registrarme", on_click=registrar),
                    ft.TextButton("Volver al login", on_click=lambda e: page.go("/")),
                    mensaje,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=15,
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
    )
