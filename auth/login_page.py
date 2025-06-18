# auth/login_page.py
import logging
import flet as ft
from auth.session import sign_in
from utils.alerts import show_snackbar

logger = logging.getLogger(__name__)


def login_page(page: ft.Page):
    # Cambiado a correo directo
    email_field = ft.TextField(label="Correo (e-mail)")
    password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)

    def on_login(e):
        if not email_field.value or not password.value:
            show_snackbar(page, "Completa todos los campos", "warning")
            return

        logger.info(f"Intentando login para: {email_field.value}")
        result = sign_in(email_field.value, password.value)

        if result["success"]:
            user = result["user"]
            session = result["session"]

            page.client_storage.set("access_token", session.access_token)
            page.client_storage.set("refresh_token", session.refresh_token)
            page.session.set("user_data", user)

            logger.info(f"Usuario autenticado: {user['nombre_usuario']}")
            show_snackbar(page, f"Bienvenido {user['nombre_usuario']}", "success")
            page.go("/home")
        else:
            logger.warning(f"Login fallido: {result['error']}")
            show_snackbar(page, f"❌ {result['error']}", "error")

    # ----- Vista ----------------------------------------------------------
    return ft.View(
        route="/",
        padding=0,
        controls=[
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Container(
                    width=400,
                    padding=30,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    shadow=ft.BoxShadow(
                        blur_radius=12,
                        color=ft.Colors.BLACK12,
                        spread_radius=1,
                        offset=ft.Offset(0, 2),
                    ),
                    content=ft.Column(
                        [
                            ft.Text("Iniciar sesión", size=24, weight=ft.FontWeight.BOLD),
                            email_field,
                            password,
                            ft.ElevatedButton("Ingresar", on_click=on_login),
                            ft.TextButton(
                                "¿No tienes cuenta? Regístrate",
                                on_click=lambda e: page.go("/register"),
                            ),
                        ],
                        spacing=15,
                        tight=True,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ),
            )
        ],
    )
