import flet as ft

def TalleresPage(page: ft.Page):
    talleres = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre del Taller")),
            ft.DataColumn(ft.Text("Profesor")),
            ft.DataColumn(ft.Text("Horas")),
        ],
        rows=[],
    )

    nombre = ft.TextField(label="Nombre del Taller")
    profesor = ft.TextField(label="Profesor")
    horas = ft.TextField(label="Horas")

    def agregar_taller(e):
        if nombre.value and profesor.value and horas.value:
            talleres.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(nombre.value)),
                        ft.DataCell(ft.Text(profesor.value)),
                        ft.DataCell(ft.Text(horas.value)),
                    ]
                )
            )
            nombre.value = profesor.value = horas.value = ""
            page.update()

    return ft.View(
        "/talleres",
        [
            ft.AppBar(title=ft.Text("Gestión de Talleres"), bgcolor=ft.colors.BLUE_300),
            ft.Column([nombre, profesor, horas, ft.ElevatedButton("Agregar", on_click=agregar_taller)], spacing=10),
            talleres,
            ft.ElevatedButton("Regresar", on_click=lambda e: page.go("/home")),
        ],
        scroll="adaptive",
    )
