import logging, flet as ft
logger = logging.getLogger(__name__)

def alistamiento_content(page: ft.Page) -> ft.Control:
    logger.info("Generando contenido Alistamiento")
    return ft.Column(
        spacing=25,
        controls=[ft.Text("Panel de Alistamiento", size=24, weight=ft.FontWeight.BOLD)],
    )
