# pages/home_page.py
import logging
import flet as ft
from components.layout import base_layout

logger = logging.getLogger(__name__)


def metric_card(title: str) -> ft.Card:
    """Crea una card informativa."""
    logger.debug(f"Creando card: {title}")
    return ft.Card(
        content=ft.Container(
            width=180,
            height=110,
            padding=15,
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.BLUE_GREY_50,
            border_radius=12,
            content=ft.Text(
                title,
                weight=ft.FontWeight.BOLD,
                size=14,
                text_align=ft.TextAlign.CENTER,
            ),
        )
    )


def home_page(page: ft.Page):
    logger.info("Cargando vista Home")

    # ─── Tarjetas resumen ────────────────────────────────────────────────
    cards = [
        metric_card("Órdenes totales"),
        metric_card("Tickets Pendientes"),
        metric_card("Alistamiento en Proceso"),
        metric_card("Serialización Pendiente"),
        metric_card("Facturas Pendientes"),
    ]
    logger.debug("Tarjetas de métricas generadas")

    # Distribución responsive
    cards_row = ft.ResponsiveRow(
        controls=[
            ft.Container(card, col={"xs": 12, "sm": 6, "md": 3, "lg": 3, "xl": 3})
            for card in cards
        ],
        run_spacing=15,
        spacing=15,
    )

    content = ft.Column(
        spacing=25,
        controls=[
            ft.Text("Panel principal", size=24, weight=ft.FontWeight.BOLD),
            cards_row,
        ],
    )

    logger.info("Home listo → devolviendo View")
    return ft.View(route="/home", padding=0, controls=[base_layout(page, content)])