# auth/session.py
import logging
from config import supabase

logger = logging.getLogger(__name__)


# ────────────────────────────────────────────────────────────────
# LOGIN
# ────────────────────────────────────────────────────────────────
def sign_in(email: str, password: str):
    """
    Autentica directamente con el correo.
    Si la fila en public.usuarios no existe aún, la crea (UPSERT).
    """
    email = email.strip().lower()
    logger.info(f"Login con correo: {email}")

    # 1. Autenticación vía Supabase Auth
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
    except Exception as exc:
        logger.error(f"Auth error: {exc}")
        return {"success": False, "error": "Credenciales inválidas o e-mail sin confirmar"}

    if not res.session:
        return {"success": False, "error": "Credenciales inválidas o e-mail sin confirmar"}

    uid = res.user.id

    # 2. Obtener o crear la fila de usuarios
    user_row = (
        supabase.table("usuarios")
        .select("*")
        .eq("auth_uid", uid)
        .single()
        .execute()
        .data
    )

    if not user_row:
        logger.info("Primera vez: insertando fila usuarios")
        user_row = {
            "auth_uid": uid,
            "email": email,
            "nombre_usuario": email.split("@")[0],
            "codigo_vendedor": "",
            "rol": "vendedor",
        }
        # UPSERT evita duplicados si la fila ya existe
        supabase.table("usuarios").upsert(user_row, on_conflict="auth_uid").execute()

    logger.info("Sesión iniciada correctamente")
    return {"success": True, "user": user_row, "session": res.session}


# ────────────────────────────────────────────────────────────────
# SIGN-UP  (sin cambios: requiere confirmar e-mail)
# ────────────────────────────────────────────────────────────────
def sign_up(email: str, password: str, nombre_usuario: str, codigo_vendedor: str):
    """
    Registra en Auth y envía correo de confirmación.
    La fila en usuarios se creará tras el primer login confirmado.
    """
    try:
        logger.info(f"Registrando: {email}")
        res = supabase.auth.sign_up({"email": email, "password": password})

        if res.user:
            return {"success": True, "pending": True}

        return {"success": False, "error": "Registro fallido"}

    except Exception as exc:
        if "User already registered" in str(exc):
            return {"success": False, "error": "Usuario ya registrado"}
        return {"success": False, "error": str(exc)}
