import flet as ft
from firebase_init import db

def HorarioVerPage(page: ft.Page):
    page.title = "Revisar Horario"

    lista = ft.Column(spacing=10)

    def cargar_horarios():
        lista.controls.clear()
        horarios = db.collection("horarios").stream()
        encontrados = False
        for h in horarios:
            data = h.to_dict()
            texto = f"{data['materia']} - {data['dia']} ({data['hora_inicio']} a {data['hora_fin']})"
            lista.controls.append(ft.Text(texto, color=ft.Colors.BLUE_600))
            encontrados = True
        if not encontrados:
            lista.controls.append(ft.Text("📭 No hay horarios registrados aún."))
        page.update()

    # Cargar al abrir la página
    cargar_horarios()

    return ft.View(
        "/horario_ver",
        [
            ft.AppBar(title=ft.Text("Mi Horario"), bgcolor=ft.Colors.BLUE_300),
            lista,
            ft.ElevatedButton("Actualizar", on_click=lambda e: cargar_horarios()),
            ft.ElevatedButton("Regresar al Chatbot", on_click=lambda e: page.go("/chatbot")),
        ],
    )
