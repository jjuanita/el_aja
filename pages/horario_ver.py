import flet as ft
from firebase_init import db
from theme_config import PRIMARY_COLOR

def HorarioVerPage(page: ft.Page):
    page.title = "Mi Horario"
    page.bgcolor = ft.Colors.WHITE

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Hora")),
            ft.DataColumn(ft.Text("Lunes")),
            ft.DataColumn(ft.Text("Martes")),
            ft.DataColumn(ft.Text("Miércoles")),
            ft.DataColumn(ft.Text("Jueves")),
            ft.DataColumn(ft.Text("Viernes")),
        ],
        rows=[],
    )

    def cargar_horario():
        horarios = list(db.collection("horarios").stream())

        horas_base = [f"{h}:00 - {h+1}:00" for h in range(7, 22)]
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

        for hora in horas_base:
            fila = [ft.DataCell(ft.Text(hora))]
            for dia in dias:
                celda = ""
                for h in horarios:
                    data = h.to_dict()
                    if data["dia"] == dia and data.get("hora") == hora:
                        celda = data.get("materia", "")
                        break
                fila.append(ft.DataCell(ft.Text(celda)))
            tabla.rows.append(ft.DataRow(cells=fila))

        page.update()

    cargar_horario()

    return ft.View(
        "/horario_ver",
        [
            ft.AppBar(title=ft.Text("Mi Horario"), bgcolor=PRIMARY_COLOR),
            ft.Container(
                content=tabla,
                padding=20,
                bgcolor=ft.Colors.BLUE_GREY_50,
                border_radius=10,
                expand=True
            ),
            ft.ElevatedButton(
                "Regresar",
                on_click=lambda e: page.go("/horario_form"),
                bgcolor=PRIMARY_COLOR,
                color=ft.Colors.WHITE,
            ),
        ],
        scroll="adaptive",
    )
