import flet as ft
from firebase_init import db
from theme_config import PRIMARY_COLOR, ACCENT_COLOR

def HorarioFormPage(page: ft.Page):
    page.title = "Registrar Horario"
    page.bgcolor = ft.Colors.BLUE_GREY_50

    usuario = page.session.get("usuario") or "anonimo@utsjr.edu.mx"

    # --- Días y horas base ---
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    horas = [f"{h}:00 - {h+1}:00" for h in range(7, 22)]

    # --- Contenedor principal del horario ---
    celdas = {}

    # Crear cabecera
    encabezados = [ft.Text("Hora", weight="bold", width=100)] + [
        ft.Text(d, weight="bold", text_align=ft.TextAlign.CENTER, width=180)
        for d in dias
    ]
    tabla = [ft.Row(encabezados, spacing=5)]

    # Crear cuadrícula editable
    for hora in horas:
        fila = [ft.Text(hora, width=100, weight="bold")]
        for dia in dias:
            clave = f"{dia}_{hora}"
            campo = ft.TextField(
                hint_text="Materia / Aula",
                width=180,
                height=40,
                border_color=PRIMARY_COLOR,
                bgcolor=ft.Colors.WHITE,
                dense=True,
            )
            celdas[clave] = campo
            fila.append(campo)
        tabla.append(ft.Row(fila, spacing=5))

    # --- Función para cargar el horario guardado ---
    def cargar_horario():
        try:
            horarios = list(db.collection("horarios").where("usuario", "==", usuario).stream())
            for h in horarios:
                data = h.to_dict()
                clave = f"{data['dia']}_{data['hora']}"
                if clave in celdas:
                    celdas[clave].value = data.get("materia", "")
            page.update()
        except Exception as ex:
            print("⚠️ Error al cargar horario:", ex)

    # --- Función para guardar (actualizar) horario ---
    def guardar_horario(e):
        datos_guardados = []
        for clave, campo in celdas.items():
            if campo.value.strip():
                dia, hora = clave.split("_")
                datos_guardados.append({
                    "usuario": usuario,
                    "dia": dia,
                    "hora": hora,
                    "materia": campo.value.strip()
                })

        if datos_guardados:
            # Borrar horario anterior del usuario
            antiguos = list(db.collection("horarios").where("usuario", "==", usuario).stream())
            for doc in antiguos:
                doc.reference.delete()

            # Guardar los nuevos
            for dato in datos_guardados:
                db.collection("horarios").add(dato)

            page.snack_bar = ft.SnackBar(
                ft.Text("✅ Horario guardado correctamente."),
                bgcolor=ACCENT_COLOR
            )
            page.snack_bar.open = True
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text("⚠️ No hay materias registradas."),
                bgcolor=ft.Colors.RED_400
            )
            page.snack_bar.open = True
        page.update()

    # --- Al entrar a la página ---
    def on_mount(e):
        cargar_horario()

    # --- Ir a ver horario ---
    def ver_horario(e):
        page.go("/horario_ver")

    # Registrar evento al montar la vista
    page.on_mount = on_mount

    # --- Layout final ---
    return ft.View(
        "/horario_form",
        [
            ft.AppBar(
                title=ft.Text("Registrar Horario", color=ft.Colors.WHITE),
                bgcolor=PRIMARY_COLOR,
                actions=[
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=ft.Colors.WHITE,
                        on_click=lambda e: page.go("/chatbot")
                    )
                ],
            ),
            ft.Container(
                padding=15,
                expand=True,
                content=ft.Column(
                    [
                        ft.Text(
                            "🗓️ Llena o edita tu horario semanal",
                            size=20,
                            weight="bold",
                            color=PRIMARY_COLOR
                        ),
                        ft.Container(
                            content=ft.Column(tabla, scroll="auto"),
                            bgcolor=ft.Colors.WHITE,
                            border_radius=10,
                            shadow=ft.BoxShadow(blur_radius=6, color=ft.Colors.GREY_400),
                            padding=10,
                            expand=True,
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "💾 Guardar horario completo",
                                    bgcolor=ACCENT_COLOR,
                                    color=ft.Colors.WHITE,
                                    on_click=guardar_horario,
                                ),
                                ft.ElevatedButton(
                                    "👁 Ver horario",
                                    bgcolor=PRIMARY_COLOR,
                                    color=ft.Colors.WHITE,
                                    on_click=ver_horario,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20,
                        ),
                    ],
                    expand=True,
                    scroll="auto",
                ),
            ),
        ],
    )
