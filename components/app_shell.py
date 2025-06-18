# components/app_shell.py
import logging
import flet as ft
from utils.alerts import show_snackbar
from config import supabase

logger = logging.getLogger(__name__)

MENU_WIDTH    = 240
CONTENT_MAX_W = 1400            # ancho máximo del panel central


def build_shell(page: ft.Page):
    """
    Crea la vista “shell” (header + drawer + footer) una sola vez y
    devuelve tres objetos:
      1. shell_view  – View completa
      2. switcher    – AnimatedSwitcher para inyectar cada página interna
      3. user_label  – Text que muestra el nombre del usuario (para actualizarlo)
    """
    # ── Estado interno ---------------------------------------------------
    menu_open = {"value": False}

    # --------------------------------------------------------------------
    # Helpers
    # --------------------------------------------------------------------
    def dx_frac() -> float:                       # ancho relativo del drawer
        return 0 if page.width == 0 else MENU_WIDTH / page.width

    def update_offsets():
        """Desplaza drawer y contenido según esté abierto o cerrado."""
        menu_container.offset = ft.Offset(0, 0) if menu_open["value"] else ft.Offset(-1, 0)
        content_container.offset = (
            ft.Offset(dx_frac(), 0) if menu_open["value"] else ft.Offset(0, 0)
        )

    def update_width():
        """Mantiene tope de anchura del panel central al redimensionar."""
        rounded_container.width = min(page.width - 40, CONTENT_MAX_W)

    # --------------------------------------------------------------------
    # Logout
    # --------------------------------------------------------------------
    def logout():
        logger.info("Cerrando sesión")
        page.client_storage.clear()
        page.session.clear()
        try:
            supabase.auth.sign_out()
        except Exception as exc:
            logger.warning(f"sign_out: {exc}")
        page.go("/")

    # --------------------------------------------------------------------
    # Drawer toggle
    # --------------------------------------------------------------------
    def toggle_menu():
        menu_open["value"] = not menu_open["value"]
        update_offsets()
        backdrop.visible = menu_open["value"]
        backdrop.opacity = 0.35 if menu_open["value"] else 0
        page.update()

    # --------------------------------------------------------------------
    # Navegación desde el drawer
    # --------------------------------------------------------------------
    def navigate_to(route: str, msg: str):
        logger.info(f"Navegando a {route}")
        toggle_menu()
        show_snackbar(page, msg, "info")
        page.go(route)              # main.route_change reemplazará contenido

    # --------------------------------------------------------------------
    # Listener de redimensionamiento
    # --------------------------------------------------------------------
    def on_resize(_):
        update_offsets()
        update_width()
        page.update()

    page.on_resize = on_resize

    # --------------------------------------------------------------------
    # HEADER
    # --------------------------------------------------------------------
    user_label = ft.Text("👤 Invitado", color=ft.Colors.WHITE)   # ← se actualizará

    header = ft.Container(
        padding=15,
        bgcolor=ft.Colors.BLUE_GREY_900,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.IconButton(
                    icon=ft.Icons.MENU,
                    icon_color=ft.Colors.WHITE,
                    on_click=lambda _: toggle_menu(),
                ),
                ft.Text("Colibrí", color=ft.Colors.WHITE, size=20, weight=ft.FontWeight.BOLD),
                ft.Container(expand=True),
                user_label,          # ← muestra nombre de usuario
            ],
        ),
    )

    # --------------------------------------------------------------------
    # DRAWER
    # --------------------------------------------------------------------
    menu_container = ft.Container(
        width=MENU_WIDTH,
        bgcolor=ft.Colors.SURFACE,
        padding=15,
        offset=ft.Offset(-1, 0),
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
            on_click=lambda _: navigate_to("/home", "🔄 Cargando resumen..."),
        ),
        ft.ListTile(
            leading=ft.Icon(ft.Icons.CLOUD_UPLOAD, color=ft.Colors.BLUE_GREY_700),
            title=ft.Text("Cargar Órdenes"),
            hover_color=ft.Colors.BLUE_GREY_100,
            on_click=lambda _: navigate_to("/upload", "🔄 Cargando módulo de carga..."),
        ),
        # ─────────── Botones nuevos ──────────────────────────────────
        ft.ListTile(  # 🆕
            leading=ft.Icon(ft.Icons.RECEIPT, color=ft.Colors.BLUE_GREY_700),
            title=ft.Text("Tickets"),
            hover_color=ft.Colors.BLUE_GREY_100,
            on_click=lambda _: navigate_to("/tickets", "🔄 Cargando tickets..."),
        ),
        ft.ListTile(  # 🆕
            leading=ft.Icon(ft.Icons.MOVING, color=ft.Colors.BLUE_GREY_700),
            title=ft.Text("Alistamiento"),
            hover_color=ft.Colors.BLUE_GREY_100,
            on_click=lambda _: navigate_to("/alistamiento", "🔄 Cargando alistamiento..."),
        ),
        ft.ListTile(  # 🆕
            leading=ft.Icon(ft.Icons.INVENTORY, color=ft.Colors.BLUE_GREY_700),
            title=ft.Text("Serialización"),
            hover_color=ft.Colors.BLUE_GREY_100,
            on_click=lambda _: navigate_to("/serializacion", "🔄 Cargando serialización..."),
        ),
        ft.ListTile(  # 🆕
            leading=ft.Icon(ft.Icons.REQUEST_PAGE, color=ft.Colors.BLUE_GREY_700),
            title=ft.Text("Facturas"),
            hover_color=ft.Colors.BLUE_GREY_100,
            on_click=lambda _: navigate_to("/facturas", "🔄 Cargando facturación..."),
        ),
        # ─────────── Fin botones nuevos ──────────────────────────────
        ft.Container(expand=True),
        ft.ElevatedButton(
            icon=ft.Icon(ft.Icons.LOGOUT_OUTLINED, color=ft.Colors.RED),
            text="Cerrar sesión",
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.TRANSPARENT,
                        elevation=0,
                        overlay_color=ft.Colors.RED_50,
                    ),
                    on_click=lambda _: logout(),
                ),
            ],
        ),
    )

    # --------------------------------------------------------------------
    # BACKDROP (oscurece el cuerpo cuando el drawer está abierto)
    # --------------------------------------------------------------------
    backdrop = ft.Container(
        expand=True,
        bgcolor=ft.Colors.BLACK,
        opacity=0,
        visible=False,
        animate_opacity=ft.Animation(300, "easeInOut"),
        on_click=lambda _: toggle_menu(),
    )

    # --------------------------------------------------------------------
    # AnimatedSwitcher – panel central que cambiará entre páginas
    # --------------------------------------------------------------------
    switcher = ft.AnimatedSwitcher(
        ft.Container(),                           # empieza vacío
        transition=ft.AnimatedSwitcherTransition.FADE,  # FADE | SLIDE | SCALE
        duration=300,
    )

    rounded_container = ft.Container(
        width=min(page.width - 40, CONTENT_MAX_W),
        bgcolor=ft.Colors.WHITE,
        border_radius=20,
        padding=25,
        content=switcher,
    )

    content_container = ft.Container(
        expand=True,
        padding=20,
        alignment=ft.alignment.top_center,
        animate_offset=ft.Animation(300, "easeInOut"),  # desplaza al abrir drawer
        content=rounded_container,
    )

    body_stack = ft.Stack(
        expand=True,
        controls=[content_container, backdrop, menu_container],
    )

    # --------------------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------------------
    footer = ft.Container(
        bgcolor=ft.Colors.BLUE_GREY_900,
        padding=10,
        alignment=ft.alignment.center,
        content=ft.Text("© 2025 Colibrí", size=12, color=ft.Colors.WHITE),
    )

    # --------------------------------------------------------------------
    # View final (shell)
    # --------------------------------------------------------------------
    shell_view = ft.View(
        route="/shell",
        padding=0,
        controls=[ft.Column(spacing=0, expand=True, controls=[header, body_stack, footer])],
    )

    # ────────────────────────────────────────────────────────────────────
    # Devuelve la View + referencias
    # ────────────────────────────────────────────────────────────────────
    return shell_view, switcher, user_label
