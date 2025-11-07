import flet as ft
from theme_config import PRIMARY_COLOR, BACKGROUND_COLOR, ACCENT_COLOR

def ChatbotPage(page: ft.Page):
    page.title = "Chatbot Académico - EL AJA"
    page.bgcolor = BACKGROUND_COLOR

    chat = ft.ListView(expand=True, spacing=10, auto_scroll=True, padding=10)

    entrada = ft.TextField(
        label="Escribe tu mensaje...",
        expand=True,
        border_color=PRIMARY_COLOR,
        on_submit=lambda e: enviar(e)  # Enviar con tecla Enter
    )

    # --- Diccionario de respuestas automáticas ---
    respuestas = {
        "mapa": ["📍 El mapa interactivo del campus estará disponible en la sección 'Mapa'."],
        "profesor": ["📧 Puedes buscar el contacto de tu profesor en el directorio académico."],
        "taller": ["🧾 Los talleres complementarios se publican cada cuatrimestre en la app."]
    }

    activadores = ["hola", "buenas", "ayuda", "menu", "menú", "empezar"]

    # --- Crear "burbujas" de mensaje ---
    def burbuja_mensaje(texto, es_usuario=False):
        color_fondo = PRIMARY_COLOR if es_usuario else ft.Colors.WHITE
        color_texto = ft.Colors.WHITE if es_usuario else ft.Colors.BLACK
        alineacion = ft.MainAxisAlignment.END if es_usuario else ft.MainAxisAlignment.START
        avatar = (
            ft.Image(src="assets/logo.png", width=40, height=40)
            if not es_usuario else ft.Container(width=40)
        )

        return ft.Row(
            alignment=alineacion,
            controls=[
                avatar if not es_usuario else ft.Container(),
                ft.Container(
                    content=ft.Text(texto, color=color_texto, size=14),
                    bgcolor=color_fondo,
                    border_radius=10,
                    padding=10,
                    width=page.width * 0.6,
                ),
            ],
        )

    # --- Crear botones dinámicamente ---
    def crear_opciones(opciones, funcion):
        return ft.Dropdown(
            options=[ft.dropdown.Option(op) for op in opciones],
            width=250,
            on_change=lambda e: funcion(e),
            label="Selecciona una opción",
            bgcolor=ft.Colors.WHITE,
            border_color=PRIMARY_COLOR,
        )

    # --- Submenús ---
    def submenu_horario():
        opciones = ["🆕 Registrar horario", "📋 Revisar horario"]
        chat.controls.append(crear_opciones(opciones, seleccionar_horario_opcion))
        page.update()

    def submenu_asesorias():
        opciones = ["📘 Matemáticas", "🧪 Física", "💻 Programación", "🧬 Biología"]
        chat.controls.append(burbuja_mensaje("Selecciona una materia para asesoría:", es_usuario=False))
        chat.controls.append(crear_opciones(opciones, seleccionar_materia))
        page.update()

    # --- Profesores disponibles ---
    def mostrar_profesores(materia):
        profesores = {
            "matemáticas": ["Dr. Ramírez", "Mtra. López"],
            "física": ["Ing. Torres", "Mtra. Pineda"],
            "programación": ["Ing. Hernández", "Lic. Gómez"],
            "biología": ["Mtro. Vargas", "Dra. Ruiz"]
        }
        lista = profesores.get(materia.lower(), [])
        if lista:
            chat.controls.append(burbuja_mensaje(f"👨‍🏫 Profesores disponibles para {materia}:", es_usuario=False))
            for prof in lista:
                chat.controls.append(burbuja_mensaje(f"• {prof}", es_usuario=False))
        else:
            chat.controls.append(burbuja_mensaje("No se encontraron profesores para esa materia.", es_usuario=False))
        page.update()

    # --- Responder texto ---
    def responder(texto_usuario):
        texto_usuario = texto_usuario.lower()
        for act in activadores:
            if act in texto_usuario:
                return [
                    "👋 ¡Hola! Soy tu asistente académico EL AJA.",
                    "¿Sobre qué tema necesitas ayuda?"
                ]
        for clave, respuesta in respuestas.items():
            if clave in texto_usuario:
                return respuesta
        return ["🤖 No entendí tu consulta. Escribe 'ayuda' o selecciona una opción."]

    # --- Cuando se selecciona una opción principal ---
    def seleccionar_opcion(e):
        opcion = e.control.value
        chat.controls.append(burbuja_mensaje(f"Tú: {opcion}", es_usuario=True))

        if "horario" in opcion.lower():
            chat.controls.append(burbuja_mensaje("¿Qué deseas hacer con tu horario?", es_usuario=False))
            submenu_horario()

        elif "asesoría" in opcion.lower():
            submenu_asesorias()

        else:
            for respuesta in responder(opcion):
                chat.controls.append(burbuja_mensaje(respuesta, es_usuario=False))

        page.update()

    # --- Subopciones de horario ---
    def seleccionar_horario_opcion(e):
        opcion = e.control.value
        chat.controls.append(burbuja_mensaje(f"Tú: {opcion}", es_usuario=True))
        if "registrar" in opcion.lower():
            chat.controls.append(burbuja_mensaje("📝 Redirigiendo al formulario de horario...", es_usuario=False))
            page.go("/horario_form")
        elif "revisar" in opcion.lower():
            chat.controls.append(burbuja_mensaje("📋 Abriendo tu horario registrado...", es_usuario=False))
            page.go("/horario_ver")
        page.update()

    # --- Subopciones de asesorías ---
    def seleccionar_materia(e):
        materia = e.control.value
        chat.controls.append(burbuja_mensaje(f"Tú: {materia}", es_usuario=True))
        mostrar_profesores(materia)

    # --- Enviar mensaje libre ---
    def enviar(e):
        if entrada.value.strip():
            msg = entrada.value.strip()
            chat.controls.append(burbuja_mensaje(f"Tú: {msg}", es_usuario=True))
            for respuesta in responder(msg):
                chat.controls.append(burbuja_mensaje(respuesta, es_usuario=False))
            if any(pal in msg.lower() for pal in activadores):
                opciones_principales = [
                    "📅 Horario de clases",
                    "👨‍🏫 Asesorías académicas",
                    "🧾 Talleres complementarios",
                    "📍 Mapa del campus",
                    "📚 Contactar a un profesor"
                ]
                chat.controls.append(crear_opciones(opciones_principales, seleccionar_opcion))
            entrada.value = ""
            page.update()

    # --- Vista principal ---
    return ft.View(
        "/chatbot",
        [
            ft.AppBar(
                title=ft.Text("Chatbot Académico", color=ft.Colors.WHITE),
                bgcolor=PRIMARY_COLOR,
                actions=[
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=ft.Colors.WHITE,
                        on_click=lambda e: page.go("/home"),
                        tooltip="Regresar",
                    )
                ],
            ),
            ft.Container(
                expand=True,
                content=ft.Column(
                    [
                        ft.Container(chat, expand=True),  # Chat ocupa todo el alto disponible
                        ft.Container(
                            content=ft.Row(
                                [
                                    entrada,
                                    ft.IconButton(
                                        icon=ft.Icons.SEND,
                                        on_click=enviar,
                                        bgcolor=PRIMARY_COLOR,
                                        icon_color=ft.Colors.WHITE,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            bgcolor=ft.Colors.WHITE,
                            padding=10,
                            border=ft.border.only(top=ft.BorderSide(1, PRIMARY_COLOR)),
                        ),
                    ],
                    expand=True,
                    spacing=0,
                ),
            ),
        ],
        scroll="adaptive",
    )
