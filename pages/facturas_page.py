import logging, flet as ft
logger = logging.getLogger(__name__)

def facturas_content(page: ft.Page) -> ft.Control:
    logger.info("Generando contenido Facturas")
    return ft.Column(
        spacing=25,
        controls=[ft.Text("Gestión de Facturas", size=24, weight=ft.FontWeight.BOLD)],
    )
