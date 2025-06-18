import flet as ft
from flet import Colors


def show_snackbar(page: ft.Page, message: str, status: str = "error"):
    """
    Muestra un SnackBar consistente que:
    1. Usa color según el estado.
    2. Evita duplicados en page.overlay.
    3. Puede invocarse desde cualquier punto sin bloquear futuros SnackBars.
    """
    # ─── Paleta de colores ───────────────────────────────────────────────
    color_map = {
        "success": Colors.GREEN,
        "error": Colors.RED,
        "info": Colors.BLUE,
        "warning": Colors.ORANGE,
    }
    txt_color = color_map.get(status, Colors.GREY)

    # ─── Construcción del SnackBar ───────────────────────────────────────
    snackbar = ft.SnackBar(
        content=ft.Text(message, color=txt_color),
        bgcolor=Colors.WHITE,
        duration=3000,
    )

    # ─── Gestión en overlay para compatibilidad total ────────────────────
    # Elimina un SnackBar previo para no acumular instancias
    if getattr(page, "snack_bar", None) and page.snack_bar in page.overlay:
        page.overlay.remove(page.snack_bar)

    # Asigna y agrega uno nuevo
    page.snack_bar = snackbar
    page.overlay.append(snackbar)

    # ─── Despliegue ───────────────────────────────────────────────────────
    snackbar.open = True
    page.update()
