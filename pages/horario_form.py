import flet as ft
from firebase_init import db

def HorarioFormPage(page: ft.Page):
    page.title = "Registrar Horario"

    # Campos del formulario
    materia = ft.TextField(label="Materia")
    profesor = ft.TextField(label="Profesor")
    dia = ft.TextField(label="Día de la semana")
    hora_inicio = ft.TextField(label="Hora de inicio")
    hora_fin = ft.TextField(label="Hora de fin")

    # Función para guardar en Firestore
    def guardar(e):
        if materia.value and dia.value:
            nuevo_horario = {
                "materia": materia.value,
                "profesor": profesor.value,
                "dia": dia.value,
                "hora_inicio": hora_inicio.value,
                "hora_fin": hora_fin.value
            }

            db.collection("horarios").add(nuevo_horario)

            page.dialog = ft.AlertDialog(
                title=ft.Text("✅ Horario guardado correctamente"),
                on_dismiss=lambda e: page.go("/chatbot")
            )
            page.dialog.open = True
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor completa al menos materia y día."))
            page.snack_bar.open = True
            page.update()

    return ft.View(
        "/horario_form",
        [
            ft.AppBar(title=ft.Text("Registrar Horario"), bgcolor=ft.Colors.BLUE_300),
            ft.Column(
                [
                    materia,
                    profesor,
                    dia,
                    hora_inicio,
                    hora_fin,
                    ft.ElevatedButton("Guardar", on_click=guardar),
                    ft.ElevatedButton("Regresar al Chatbot", on_click=lambda e: page.go("/chatbot")),
                ],
                spacing=10,
            ),
        ],
    )
