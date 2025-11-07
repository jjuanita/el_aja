import flet as ft
from firebase_init import db
from theme_config import PRIMARY_COLOR, ACCENT_COLOR
from datetime import datetime

def ForoPage(page: ft.Page):
    page.title = "Foro Académico - EL AJA"
    page.bgcolor = ft.Colors.BLUE_GREY_50

    usuario = page.session.get("usuario") or "usuario@utsjr.edu.mx"

    mensajes = ft.Column(scroll="auto", expand=True, spacing=10)
    entrada = ft.TextField(
        label="Escribe tu pregunta o comentario...",
        expand=True,
        border_color=PRIMARY_COLOR,
        focused_border_color=ACCENT_COLOR,
        cursor_color=ACCENT_COLOR,
    )

    # --- Función para mostrar mensajes ---
    def render_mensajes(snapshot):
        mensajes.controls.clear()
        for doc in snapshot:
            data = doc.to_dict()

            # Obtener subcolección de respuestas
            respuestas = []
            subres = db.collection("foro").document(doc.id).collection("respuestas").order_by("timestamp").stream()
            for r in subres:
                rdata = r.to_dict()
                respuestas.append(
                    ft.Container(
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=10,
                        padding=8,
                        margin=ft.margin.only(left=25, top=5, bottom=5),
                        content=ft.Text(f"💬 {rdata['usuario']}: {rdata['mensaje']}")
                    )
                )

            # Campo para responder
            respuesta_field = ft.TextField(
                hint_text="Escribe una respuesta...",
                width=400,
                dense=True,
            )

            def responder_click(e, doc_id=doc.id):
                if respuesta_field.value.strip():
                    db.collection("foro").document(doc_id).collection("respuestas").add({
                        "usuario": usuario,
                        "mensaje": respuesta_field.value.strip(),
                        "timestamp": datetime.now()
                    })
                    respuesta_field.value = ""
                    cargar_respuestas_en_vivo()  # 🔄 actualiza dinámicamente

            mensajes.controls.append(
                ft.Container(
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    shadow=ft.BoxShadow(blur_radius=4, color=ft.Colors.GREY_400),
                    padding=10,
                    content=ft.Column([
                        ft.Text(f"👤 {data['usuario']}", weight="bold", color=PRIMARY_COLOR),
                        ft.Text(data["mensaje"], size=15),
                        ft.Text(f"🕒 {data['fecha']}", size=12, italic=True, color=ft.Colors.GREY_600),
                        ft.Row([
                            respuesta_field,
                            ft.IconButton(icon=ft.Icons.SEND, on_click=lambda e, id=doc.id: responder_click(e, id), icon_color=ACCENT_COLOR)
                        ]),
                        *respuestas
                    ])
                )
            )

        page.update()

    # --- Listener en tiempo real ---
    def cargar_mensajes_en_vivo():
        db.collection("foro").order_by("timestamp").on_snapshot(lambda col_snapshot, changes, read_time: render_mensajes(col_snapshot))

    # --- Listener para respuestas ---
    def cargar_respuestas_en_vivo():
        cargar_mensajes_en_vivo()

    # --- Publicar nuevo mensaje ---
    def enviar_mensaje(e):
        if entrada.value.strip():
            db.collection("foro").add({
                "usuario": usuario,
                "mensaje": entrada.value.strip(),
                "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "timestamp": datetime.now()
            })
            entrada.value = ""
            page.update()

    # --- Iniciar escucha al montar la página ---
    def on_mount(e):
        cargar_mensajes_en_vivo()

    page.on_mount = on_mount

    # --- Layout principal ---
    return ft.View(
        "/foro",
        [
            ft.AppBar(
                title=ft.Text("Foro Académico"),
                bgcolor=PRIMARY_COLOR,
                color=ft.Colors.WHITE,
                actions=[
                    ft.IconButton(
                        icon=ft.Icons.REFRESH,
                        icon_color=ft.Colors.WHITE,
                        on_click=lambda e: cargar_mensajes_en_vivo(),
                        tooltip="Actualizar foro"
                    )
                ]
            ),
            ft.Container(
                content=mensajes,
                padding=15,
                expand=True,
            ),
            ft.Container(
                bgcolor=ft.Colors.WHITE,
                border_radius=10,
                shadow=ft.BoxShadow(blur_radius=6, color=ft.Colors.GREY_400),
                padding=10,
                content=ft.Row(
                    [entrada, ft.IconButton(icon=ft.Icons.SEND, on_click=enviar_mensaje, icon_color=ACCENT_COLOR)],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ),
            ft.ElevatedButton(
                "Regresar",
                on_click=lambda e: page.go("/home"),
                bgcolor=ACCENT_COLOR,
                color=ft.Colors.WHITE,
            ),
        ],
        scroll="adaptive",
    )
