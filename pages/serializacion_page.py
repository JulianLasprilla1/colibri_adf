import logging, flet as ft
logger = logging.getLogger(__name__)

def serializacion_content(page: ft.Page) -> ft.Control:
    logger.info("Generando contenido Serialización")
    return ft.Column(
        spacing=25,
        controls=[ft.Text("Panel de Serialización", size=24, weight=ft.FontWeight.BOLD)],
    )
