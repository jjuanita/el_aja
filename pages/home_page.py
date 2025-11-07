import flet as ft
from firebase_init import db
from theme_config import PRIMARY_COLOR, ACCENT_COLOR

def HomePage(page: ft.Page):
    page.title = "Menú Principal - EL AJA"
    page.bgcolor = ft.Colors.BLUE_GREY_50

    usuario = page.session.get("usuario") or "usuario@utsjr.edu.mx"

    # --- Cargar publicaciones ---
    try:
        publicaciones = list(db.collection("foro").where("usuario", "==", usuario).stream())
        publicaciones_usuario = len(publicaciones)
    except Exception as e:
        print("Error al cargar publicaciones:", e)
        publicaciones_usuario = 0

    # Estado del menú
    menu_visible = False

    def toggle_menu(e):
        nonlocal menu_visible
        menu_visible = not menu_visible
        menu_container.visible = menu_visible
        page.update()

    def toggle_and_go(ruta):
        nonlocal menu_visible
        menu_visible = False
        menu_container.visible = False
        page.update()
        page.go(ruta)

    # --- Menú flotante sobre la pantalla ---
    menu_container = ft.Container(
        visible=False,
        bgcolor=PRIMARY_COLOR,
        border_radius=10,
        padding=12,
        width=220,
        right=10,
        top=60,
        content=ft.Column(
            [
                ft.Text("Menú principal", color=ft.Colors.WHITE, size=16, weight="bold"),
                ft.Divider(color=ft.Colors.WHITE24),
                ft.TextButton("🏠 Inicio", on_click=lambda e: toggle_and_go("/home"), style=ft.ButtonStyle(color=ft.Colors.WHITE)),
                ft.TextButton("💬 Foro Académico", on_click=lambda e: toggle_and_go("/foro"), style=ft.ButtonStyle(color=ft.Colors.WHITE)),
                ft.TextButton("🤖 Chatbot Interactivo", on_click=lambda e: toggle_and_go("/chatbot"), style=ft.ButtonStyle(color=ft.Colors.WHITE)),
                ft.TextButton("🧾 Gestión de Talleres", on_click=lambda e: toggle_and_go("/talleres"), style=ft.ButtonStyle(color=ft.Colors.WHITE)),
                ft.TextButton("🔓 Cerrar sesión", on_click=lambda e: toggle_and_go("/"), style=ft.ButtonStyle(color=ft.Colors.WHITE)),
            ],
            spacing=5,
        ),
        shadow=ft.BoxShadow(
            blur_radius=8,
            spread_radius=1,
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
        ),
    )

    # --- Crear tarjetas ---
    def crear_tarjeta(icono, titulo, descripcion, color, accion):
        return ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=6, color=ft.Colors.GREY_400),
            padding=15,
            on_click=accion,
            content=ft.Column(
                [
                    ft.Icon(icono, size=38, color=color),
                    ft.Text(titulo, size=15, weight="bold", color=color),
                    ft.Text(descripcion, size=12, color=ft.Colors.GREY_700),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            width=150,
            height=120,
        )

    # --- Barra superior ---
    top_bar = ft.Container(
        bgcolor=PRIMARY_COLOR,
        padding=ft.padding.symmetric(horizontal=15, vertical=10),
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Image(src="assets/logo.png", width=45, height=45),
                        ft.Text("EL AJA", size=20, weight="bold", color=ft.Colors.WHITE),
                    ],
                    spacing=8,
                ),
                ft.IconButton(
                    icon=ft.Icons.MENU,
                    icon_color=ft.Colors.WHITE,
                    tooltip="Menú",
                    on_click=toggle_menu,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )

    # --- Contenido principal ---
    tarjetas = ft.ResponsiveRow(
        controls=[
            crear_tarjeta(
                ft.Icons.SCHEDULE,
                "Mi horario",
                "Consulta tus clases",
                PRIMARY_COLOR,
                lambda e: page.go("/horario_ver"),
            ),
            crear_tarjeta(
                ft.Icons.FORUM,
                "Foro académico",
                f"{publicaciones_usuario} publicaciones",
                ACCENT_COLOR,
                lambda e: page.go("/foro"),
            ),
            crear_tarjeta(
                ft.Icons.WORK,
                "Talleres",
                "Gestión de talleres",
                ft.Colors.TEAL_600,
                lambda e: page.go("/talleres"),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
        run_spacing=10,
    )

    contenido = ft.Container(
        padding=ft.padding.all(20),
        expand=True,
        content=ft.Column(
            [
                ft.Image(src="assets/logo.png", width=90, height=90),
                ft.Text(
                    f"Bienvenido(a), {usuario.split('@')[0].capitalize()} 👋",
                    size=22,
                    weight="bold",
                    text_align="center",
                ),
                ft.Text(
                    "Selecciona un módulo para continuar:",
                    size=14,
                    color=ft.Colors.GREY_700,
                    text_align="center",
                ),
                ft.Divider(thickness=1, color=ft.Colors.GREY_300),
                tarjetas,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        ),
    )

    # --- Stack para superponer el menú sin mover elementos ---
    stack = ft.Stack(
        controls=[
            ft.Column([top_bar, contenido]),
            menu_container,  # Menú flotante arriba del contenido
        ],
        expand=True,
    )

    return ft.View("/home", [stack])
