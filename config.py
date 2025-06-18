# config.py
import os
from pathlib import Path
from typing import Final, Optional

from supabase import create_client, Client

# ─── Cargar .env en desarrollo ───────────────────────────────────────────
try:
    from dotenv import load_dotenv

    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    # python-dotenv solo se instala en desarrollo
    pass

# ─── Variables de entorno obligatorias ──────────────────────────────────
SUPABASE_URL: Final[str] = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY: Final[str] = os.getenv("SUPABASE_ANON_KEY", "")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise RuntimeError(
        "Variables SUPABASE_URL y/o SUPABASE_ANON_KEY no definidas."
        "  ➜ Crea un archivo .env o expórtalas en tu entorno."
    )

# ─── Cliente Supabase con clave anónima (frontend) ───────────────────────
supabase: Final[Client] = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# ─── Service role key (opcional) ─────────────────────────────────────────
SUPABASE_SERVICE_KEY: Final[Optional[str]] = os.getenv("SUPABASE_SERVICE_KEY")
