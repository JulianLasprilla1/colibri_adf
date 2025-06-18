import logging
import flet as ft
from auth.session import sign_up
from utils.alerts import show_snackbar
from config import supabase

logger = logging.getLogger(__name__)


def register_page(page: ft.Page):
    # ── Campos -----------------------------------------------------------------
    email = ft.TextField(label="Correo", on_change=lambda e: validate_ui())
    nombre_usuario = ft.TextField(label="Nombre de usuario", on_change=lambda e: validate_ui())
    codigo_vendedor = ft.TextField(label="Código de vendedor", on_change=lambda e: validate_ui())
    password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True,
                            on_change=lambda e: validate_ui())
    confirm = ft.TextField(label="Confirmar contraseña", password=True, can_reveal_password=True,
                           on_change=lambda e: validate_ui())

    btn_enviar    = ft.ElevatedButton("Enviar correo de verificación", on_click=lambda e: on_send_email(),
                                      disabled=True)
    btn_validar   = ft.ElevatedButton("Validar correo", on_click=lambda e: on_validate_email(),
                                      disabled=True)
    btn_registrar = ft.ElevatedButton("Registrar perfil", on_click=lambda e: on_register_profile(),
                                      disabled=True)

    # Guardaremos aquí el UID después de validar
    validated_user_id = {"id": None}

    # ── Validación UI ----------------------------------------------------------
    def validate_ui():
        filled = all(f.value.strip() for f in [email, nombre_usuario, codigo_vendedor, password, confirm])
        same_pw = password.value == confirm.value
        btn_enviar.disabled = not (filled and same_pw)
        if confirm.value and not same_pw:
            show_snackbar(page, "Las contraseñas no coinciden", "warning")
        page.update()

    # ── Paso 1: sign_up --------------------------------------------------------
    def on_send_email():
        logger.info("[REGISTER] Enviando correo de verificación")
        res = sign_up(email.value, password.value, nombre_usuario.value, codigo_vendedor.value)

        if res["success"]:
            show_snackbar(page, "📧 Revisa tu correo y confírmalo.", "info")
            btn_enviar.disabled = True
            btn_validar.disabled = False
            page.update()
        else:
            show_snackbar(page, f"❌ {res['error']}", "error")

    # ── Paso 2: validar correo -------------------------------------------------
    def on_validate_email():
        logger.info("[REGISTER] Intentando login para validar correo")
        try:
            login_res = supabase.auth.sign_in_with_password(
                {"email": email.value, "password": password.value}
            )
        except Exception as exc:
            msg = str(exc)
            logger.warning(f"Validación falló: {msg}")
            if "Email not confirmed" in msg:
                show_snackbar(page, "⚠️ Aún no confirmas el correo.", "warning")
            else:
                show_snackbar(page, f"❌ {msg}", "error")
            return

        if not login_res.session:
            show_snackbar(page, "⚠️ Aún no confirmas el correo.", "warning")
            return

        # Sesión válida  → guardamos UID y habilitamos Registrar perfil
        validated_user_id["id"] = login_res.user.id
        supabase.auth.set_session(login_res.session.access_token, login_res.session.refresh_token)
        show_snackbar(page, "✅ Correo confirmado. Ahora puedes registrar tu perfil.", "success")
        btn_validar.disabled = True
        btn_registrar.disabled = False
        page.update()

    # ── Paso 3: insertar fila en usuarios -------------------------------------
    def on_register_profile():
        logger.info("[REGISTER] Creando fila en public.usuarios")
        try:
            supabase.table("usuarios").insert(
                {
                    "auth_uid": validated_user_id["id"],
                    "email": email.value,
                    "nombre_usuario": nombre_usuario.value,
                    "codigo_vendedor": codigo_vendedor.value,
                    "rol": "vendedor",
                }
            ).execute()
            show_snackbar(page, "✅ Perfil creado. Inicia sesión.", "success")
            page.go("/")
        except Exception as exc:
            logger.error(f"INSERT falló: {exc}")
            show_snackbar(page, f"❌ {exc}", "error")

    # ── Render -----------------------------------------------------------------
    validate_ui()  # Estado inicial botones

    return ft.View(
        route="/register",
        padding=0,
        controls=[
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Container(
                    width=400,
                    padding=30,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    shadow=ft.BoxShadow(
                        blur_radius=12, color=ft.Colors.BLACK12, spread_radius=1, offset=ft.Offset(0, 2)
                    ),
                    content=ft.Column(
                        [
                            ft.Text("Registro de usuario", size=24, weight=ft.FontWeight.BOLD),
                            nombre_usuario,
                            codigo_vendedor,
                            email,
                            password,
                            confirm,
                            btn_enviar,
                            btn_validar,
                            btn_registrar,
                            ft.TextButton("Volver al login", on_click=lambda e: page.go("/")),
                        ],
                        spacing=15,
                        tight=True,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ),
            )
        ],
    )
