# pages/upload_page.py
import logging
import flet as ft
logger = logging.getLogger(__name__)


def upload_content(page: ft.Page) -> ft.Control:
    logger.info("Generando contenido Upload")
    return ft.Column(
        spacing=25,
        controls=[
            ft.Text("Carga y vista previa de órdenes", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(
                alignment=ft.alignment.center,
                content=ft.Text(
                    "Aquí irá el flujo de carga y vista previa.",
                    size=18,
                    text_align=ft.TextAlign.CENTER,
                ),
            ),
        ],
    )
