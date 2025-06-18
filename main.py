# main.py
import logging
import flet as ft
from config import supabase

# Páginas Auth
from auth.login_page import login_page
from auth.register_page import register_page
from pages.tickets_page import tickets_content
from pages.alistamiento_page import alistamiento_content
from pages.serializacion_page import serializacion_content
from pages.facturas_page import facturas_content
# Shell y contenidos
from components.app_shell import build_shell
from pages.home_page import home_content
from pages.upload_page import upload_content

# ── Logging global -------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def main(page: ft.Page):
    # ── Restaurar sesión (si hay JWT) -----------------------------------
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

    # ── Configuración general de la página ------------------------------
    page.title      = "Colibrí - Web"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding    = 0
    page.margin     = 0
    page.drawer     = None

    # ── Construir el ‘shell’ una sola vez -------------------------------
    shell_view, switcher, user_label = build_shell(page)

    # ── Rutas protegidas -------------------------------------------------
    protected_routes = {
        "/home",
        "/upload",
        "/tickets",
        "/alistamiento",
        "/serializacion",
        "/facturas",
    }

    def is_authenticated() -> bool:
        return bool(page.session.get("user_data"))

    def refresh_user_label():
        user = page.session.get("user_data") or {}
        user_label.value = f"👤 {user.get('nombre_usuario', 'Invitado')}"

    
    # ── Navegación -------------------------------------------------------
    def route_change(event):
        route = event.data
        logger.info(f"Cambio de ruta → {route}")

        # Rutas que requieren sesión
        if route in protected_routes and not is_authenticated():
            page.views.clear()
            page.views.append(login_page(page))
            page.update()                 # ←
            page.go("/")
            return

        # ---------- Vistas SIN shell ----------
        if route == "/":
            page.views.clear()
            page.views.append(login_page(page))
            page.update()                 # ←
            return

        if route == "/register":
            page.views.clear()
            page.views.append(register_page(page))
            page.update()                 # ←
            return

        # ---------- Vistas DENTRO del shell ----------
        if not page.views or page.views[-1].route != "/shell":
            page.views.clear()
            page.views.append(shell_view)
        refresh_user_label()

        if route == "/home":
            switcher.content = home_content(page)
        elif route == "/upload":
            switcher.content = upload_content(page)
        elif route == "/tickets":
            switcher.content = tickets_content(page)
        elif route == "/alistamiento":
            switcher.content = alistamiento_content(page)
        elif route == "/serializacion":
            switcher.content = serializacion_content(page)
        elif route == "/facturas":
            switcher.content = facturas_content(page)
        else:
            switcher.content = ft.Container()

        page.update()                     # ← siempre actualiza

    page.on_route_change = route_change
    page.go("/")


# Ejecutar
ft.app(target=main, view=ft.WEB_BROWSER)
