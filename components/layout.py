# components/layout.py
import logging
import flet as ft
from utils.alerts import show_snackbar
from config import supabase

logger = logging.getLogger(__name__)

MENU_WIDTH = 240          # ancho del drawer
CONTENT_MAX_W = 1200      # límite máximo del panel central


def base_layout(page: ft.Page, inner_content: ft.Control):
    # ─── Estado interno ───────────────────────────────────────────────────
    menu_open = {"value": False}

    # ─── Helpers ──────────────────────────────────────────────────────────
    def dx_frac() -> float:
        """Fracción del ancho de ventana que equivale a MENU_WIDTH."""
        return 0 if page.width == 0 else MENU_WIDTH / page.width

    def update_offsets():
        """Desplaza drawer y contenedor central según estado."""
        menu_container.offset = ft.Offset(0, 0) if menu_open["value"] else ft.Offset(-1, 0)
        content_container.offset = (
            ft.Offset(dx_frac(), 0) if menu_open["value"] else ft.Offset(0, 0)
        )

    def update_width():
        """Limita ancho del panel central."""
        rounded_container.width = min(page.width - 40, CONTENT_MAX_W)

    # ─── Logout global ────────────────────────────────────────────────────
    def logout():
        logger.info("Cerrando sesión")
        # 1. Elimina JWT guardados
        page.client_storage.remove("access_token")
        page.client_storage.remove("refresh_token")
        # 2. Limpia datos de usuario en sesión
        page.session.clear()
        # 3. Cierra sesión en Supabase
        try:
            supabase.auth.sign_out()
        except Exception as exc:
            logger.warning(f"sign_out: {exc}")
        # 4. Redirige
        page.go("/")

    # ─── Callbacks principales ────────────────────────────────────────────
    def toggle_menu():
        menu_open["value"] = not menu_open["value"]
        state = "abriendo" if menu_open["value"] else "cerrando"
        logger.info(f"Drawer {state}")

        update_offsets()

        # Backdrop fade
        if menu_open["value"]:
            backdrop.visible, backdrop.opacity = True, 0.35
        else:
            backdrop.opacity = 0
            page.update()
            backdrop.visible = False

        page.update()

    def navigate_to(route: str, msg: str):
        logger.info(f"Navegando a {route}")
        toggle_menu()
        show_snackbar(page, msg, "info")
        page.go(route)

    # Ventana redimensionada
    def on_resize(e):
        logger.debug(f"Resize → {page.width}×{page.height}")
        update_offsets()
        update_width()
        page.update()

    page.on_resize = on_resize

    # ─── Header ───────────────────────────────────────────────────────────
    user = page.session.get("user_data") or {}
    header = ft.Container(
        padding=15,
        bgcolor=ft.Colors.BLUE_GREY_900,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.IconButton(
                    icon=ft.Icons.MENU,
                    icon_color=ft.Colors.WHITE,
                    on_click=lambda e: toggle_menu(),
                ),
                ft.Text("Colibrí", color=ft.Colors.WHITE, size=20, weight=ft.FontWeight.BOLD),
                ft.Container(expand=True),
                ft.Text(f"👤 {user.get('nombre_usuario', 'Invitado')}", color=ft.Colors.WHITE),
            ],
        ),
    )

    # ─── Drawer ───────────────────────────────────────────────────────────
    menu_container = ft.Container(
        width=MENU_WIDTH,
        bgcolor=ft.Colors.SURFACE,
        padding=15,
        offset=ft.Offset(-1, 0),  # Oculto al iniciar
        animate_offset=ft.Animation(300, "easeInOut"),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        content=ft.Column(
            expand=True,
            controls=[
                ft.Text("Menú", size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.HOME, color=ft.Colors.BLUE_GREY_700),
                    title=ft.Text("Resumen"),
                    hover_color=ft.Colors.BLUE_GREY_100,
                    on_click=lambda e: navigate_to("/home", "🔄 Cargando resumen..."),
                ),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    icon=ft.Icon(ft.Icons.LOGOUT_OUTLINED, color=ft.Colors.RED),
                    text="Cerrar sesión",
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.TRANSPARENT, elevation=0, overlay_color=ft.Colors.RED_50
                    ),
                    on_click=lambda e: logout(),   # ← logout completo
                ),
            ],
        ),
    )

    # ─── Backdrop ─────────────────────────────────────────────────────────
    backdrop = ft.Container(
        expand=True,
        bgcolor=ft.Colors.BLACK,
        opacity=0,
        visible=False,
        animate_opacity=ft.Animation(300, "easeInOut"),
        on_click=lambda e: toggle_menu(),
    )

    # ─── Panel central ────────────────────────────────────────────────────
    rounded_container = ft.Container(
        width=min(page.width - 40, CONTENT_MAX_W),
        bgcolor=ft.Colors.WHITE,
        border_radius=20,
        padding=25,
        content=inner_content,
    )

    content_container = ft.Container(
        expand=True,
        padding=20,
        alignment=ft.alignment.top_center,
        offset=ft.Offset(0, 0),
        animate_offset=ft.Animation(300, "easeInOut"),
        content=rounded_container,
    )

    # ─── Stack principal ─────────────────────────────────────────────────
    body_stack = ft.Stack(expand=True, controls=[content_container, backdrop, menu_container])

    # ─── Footer ───────────────────────────────────────────────────────────
    footer = ft.Container(
        bgcolor=ft.Colors.BLUE_GREY_900,
        padding=10,
        alignment=ft.alignment.center,
        content=ft.Text("© 2025 Colibrí", size=12, color=ft.Colors.WHITE),
    )

    # ─── Ensamblaje final ─────────────────────────────────────────────────
    return ft.Column(spacing=0, expand=True, controls=[header, body_stack, footer])
