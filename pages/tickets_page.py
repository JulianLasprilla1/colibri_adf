import logging, flet as ft
logger = logging.getLogger(__name__)

def tickets_content(page: ft.Page) -> ft.Control:
    logger.info("Generando contenido Tickets")
    return ft.Column(
        spacing=25,
        controls=[ft.Text("Gestión de Tickets", size=24, weight=ft.FontWeight.BOLD)],
    )
