import flet as ft
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.foro_page import ForoPage
from pages.chatbot_page import ChatbotPage
from pages.talleres_page import TalleresPage
from pages.horario_form import HorarioFormPage
from pages.horario_ver import HorarioVerPage
from pages.register_page import RegisterPage



def main(page: ft.Page):
    page.title = "EL AJA - Asistente Virtual Académico"
    page.theme_mode = "light"
    page.scroll = "adaptive"
    page.padding = 10

    # --- Control de navegación entre pantallas ---
    def route_change(route):
        page.views.clear()

        if page.route == "/":
            page.views.append(LoginPage(page))
        elif page.route == "/register":
            page.views.append(RegisterPage(page))
        elif page.route == "/home":
            page.views.append(HomePage(page))
        elif page.route == "/foro":
            page.views.append(ForoPage(page))
        elif page.route == "/chatbot":
            page.views.append(ChatbotPage(page))
        elif page.route == "/horario_form":
            from pages.horario_form import HorarioFormPage
            page.views.append(HorarioFormPage(page))
        elif page.route == "/horario_ver":
            from pages.horario_ver import HorarioVerPage
            page.views.append(HorarioVerPage(page))
        elif page.route == "/talleres":
            page.views.append(TalleresPage(page))
        else:
            page.views.append(ft.View("/", [ft.Text("Ruta no encontrada")]))

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main, view=ft.WEB_BROWSER)

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)