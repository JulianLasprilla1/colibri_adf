# pages/home_page.py
import logging
import flet as ft

logger = logging.getLogger(__name__)


def metric_card(title: str) -> ft.Card:
    return ft.Card(
        content=ft.Container(
            width=180,
            height=110,
            padding=15,
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.BLUE_GREY_50,
            border_radius=12,
            content=ft.Text(title, weight=ft.FontWeight.BOLD, size=14, text_align=ft.TextAlign.CENTER),
        )
    )


def home_content(page: ft.Page) -> ft.Control:
    """
    Devuelve SOLO el contenido interno. El shell lo envolverá.
    """
    logger.info("Generando contenido Home")

    cards = [
        metric_card("Órdenes totales"),
        metric_card("Tickets Pendientes"),
        metric_card("Alistamiento en Proceso"),
        metric_card("Serialización Pendiente"),
        metric_card("Facturas Pendientes"),
    ]

    cards_row = ft.ResponsiveRow(
        controls=[ft.Container(c, col={"xs": 12, "sm": 6, "md": 3, "lg": 3, "xl": 3}) for c in cards],
        run_spacing=15,
        spacing=15,
    )

    return ft.Column(
        spacing=25,
        controls=[
            ft.Text("Panel principal", size=24, weight=ft.FontWeight.BOLD),
            cards_row,
        ],
    )
