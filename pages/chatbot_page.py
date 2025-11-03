import flet as ft

def ChatbotPage(page: ft.Page):
    page.title = "Chatbot Académico - EL AJA"

    chat = ft.Column(scroll="always", expand=True)
    entrada = ft.TextField(label="Escribe tu mensaje...", expand=True)

    # --- Diccionario de respuestas automáticas ---
    respuestas = {
        "mapa": "📍 El mapa interactivo del campus estará disponible en la sección 'Mapa'.",
        "profesor": "📧 Puedes buscar el contacto de tu profesor en el directorio académico.",
        "taller": "🧾 Los talleres complementarios se publican cada cuatrimestre en la app."
    }

    activadores = ["hola", "buenas", "ayuda", "menu", "menú", "empezar"]

    # --- Crear botones dinámicamente ---
    def crear_opciones(opciones, funcion):
        return ft.Row(
            controls=[ft.ElevatedButton(op, data=op, on_click=funcion) for op in opciones],
            wrap=True,
        )

    # --- Generar submenús dinámicos ---
    def submenu_horario():
        opciones = ["🆕 Registrar horario", "📋 Revisar horario"]
        chat.controls.append(crear_opciones(opciones, seleccionar_horario_opcion))
        page.update()

    def submenu_asesorias():
        opciones = ["📘 Matemáticas", "🧪 Física", "💻 Programación", "🧬 Biología"]
        chat.controls.append(ft.Text("Selecciona una materia para asesoría:", color=ft.Colors.BLUE_600))
        chat.controls.append(crear_opciones(opciones, seleccionar_materia))
        page.update()

    def mostrar_profesores(materia):
        profesores = {
            "matemáticas": ["Dr. Ramírez", "Mtra. López"],
            "física": ["Ing. Torres", "Mtra. Pineda"],
            "programación": ["Ing. Hernández", "Lic. Gómez"],
            "biología": ["Mtro. Vargas", "Dra. Ruiz"]
        }
        lista = profesores.get(materia.lower(), [])
        if lista:
            chat.controls.append(ft.Text(f"👨‍🏫 Profesores disponibles para {materia}:", weight="bold"))
            for prof in lista:
                chat.controls.append(ft.Text(f"• {prof}", color=ft.Colors.BLUE_600))
        else:
            chat.controls.append(ft.Text("No se encontraron profesores para esa materia."))
        page.update()

    # --- Responder texto ---
    def responder(texto_usuario):
        texto_usuario = texto_usuario.lower()
        for clave, respuesta in respuestas.items():
            if clave in texto_usuario:
                return respuesta
        for act in activadores:
            if act in texto_usuario:
                return "👋 ¡Hola! Soy tu asistente académico. Elige una opción para comenzar:"
        return "🤖 No entendí tu consulta. Escribe 'ayuda' o selecciona una opción."

    # --- Cuando se selecciona una opción principal ---
    def seleccionar_opcion(e):
        opcion = e.control.data
        chat.controls.append(ft.Text(f"👤 Tú: {opcion}", weight="bold"))

        if "horario" in opcion.lower():
            chat.controls.append(ft.Text("¿Qué deseas hacer con tu horario?", color=ft.Colors.BLUE_600))
            submenu_horario()

        elif "asesoría" in opcion.lower():
            submenu_asesorias()

        else:
            respuesta_bot = responder(opcion)
            chat.controls.append(ft.Text(respuesta_bot, color=ft.Colors.BLUE_600))

        page.update()

    # --- Subopciones de horario ---
    def seleccionar_horario_opcion(e):
        opcion = e.control.data
        chat.controls.append(ft.Text(f"👤 Tú: {opcion}", weight="bold"))

        if "registrar" in opcion.lower():
            chat.controls.append(ft.Text("📝 Redirigiendo al formulario de horario..."))
            page.go("/horario_form")

        elif "revisar" in opcion.lower():
            chat.controls.append(ft.Text("📋 Abriendo tu horario registrado..."))
            page.go("/horario_ver")

        page.update()

    # --- Subopciones de asesorías ---
    def seleccionar_materia(e):
        materia = e.control.data
        chat.controls.append(ft.Text(f"👤 Tú: {materia}", weight="bold"))
        mostrar_profesores(materia)

    # --- Enviar mensaje libre ---
    def enviar(e):
        if entrada.value.strip():
            msg = entrada.value.strip()
            chat.controls.append(ft.Text(f"👤 Tú: {msg}", weight="bold"))
            respuesta_bot = responder(msg)
            chat.controls.append(ft.Text(respuesta_bot, color=ft.Colors.BLUE_600))
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
            ft.AppBar(title=ft.Text("Chatbot Académico"), bgcolor=ft.Colors.BLUE_300),
            chat,
            ft.Row([entrada, ft.IconButton(icon=ft.Icons.SEND, on_click=enviar)]),
            ft.ElevatedButton("Regresar", on_click=lambda e: page.go("/home")),
        ],
        scroll="adaptive",
    )
