# main.py
import logging
import flet as ft
from config import supabase
from auth.login_page import login_page
from auth.register_page import register_page
from pages.home_page import home_page

# ─── Configurar logging global ───────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def main(page: ft.Page):
    # ---------- Restaurar sesión si hay JWT ----------
    access_token = page.client_storage.get("access_token")
    refresh_token = page.client_storage.get("refresh_token")

    if access_token and refresh_token:
        try:
            supabase.auth.set_session(access_token, refresh_token)
            new_session = supabase.auth.refresh_session()
            if new_session:
                page.client_storage.set("access_token", new_session.access_token)
                page.client_storage.set("refresh_token", new_session.refresh_token)
            logger.info("Sesión restaurada desde client_storage")
        except Exception as exc:
            logger.warning(f"Tokens inválidos: {exc}")
            page.client_storage.clear()

    # ---------- Configuración general ----------
    page.title = "Colibrí - Web"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.margin = 0
    page.drawer = None

    # ---------- Guardas de autenticación ----------
    def is_authenticated() -> bool:
        return bool(page.session.get("user_data"))

    protected_routes = {"/home"}

    # ---------- Navegación ----------
    def route_change(event):
        route = event.data
        logger.info(f"Cambio de ruta → {route}")
        page.views.clear()

        # Redirige a login si intenta acceder a ruta protegida sin sesión
        if route in protected_routes and not is_authenticated():
            page.views.append(login_page(page))
            page.go("/")
            page.update()
            return

        if route == "/":
            page.views.append(login_page(page))
        elif route == "/register":
            page.views.append(register_page(page))
        elif route == "/home":
            page.views.append(home_page(page))
        else:
            page.views.append(login_page(page))
            page.go("/")

        page.update()

    page.on_route_change = route_change
    page.go("/")


# Ejecutar en modo web
ft.app(target=main, view=ft.WEB_BROWSER)
