from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()  # ✅ Esto usa la función y elimina la advertencia

# =====================================
# CONFIGURADOR AUTOMÁTICO DE ENTORNO DJANGO (.env + settings.py)
# =====================================

os.getenv(
    "NOMBRE_DE_VARIABLE"
)  # ejemplo de uso (mantiene el import 'os' activo)

BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / '.env'

# Busca el archivo settings.py (normalmente dentro de "mysite" o similar)
settings_path = None
for subfolder in BASE_DIR.iterdir():
    if subfolder.is_dir():
        possible = subfolder / 'settings.py'
        if possible.exists():
            settings_path = possible
            break

# 1️⃣ Crear o actualizar el archivo .env
env_content = """# ==========================
# CONFIGURACIÓN DEL PROYECTO DJANGO
# ==========================

# --- Clave secreta de Django ---
SECRET_KEY=djangosecretkey1234567890

# --- Modo debug ---
DEBUG=True

# --- Selecciona motor de base de datos ---
# Opciones: sqlite o postgres
DB_ENGINE=sqlite

# --- Configuración para SQLite ---
DB_NAME=db.sqlite3

# --- Configuración para PostgreSQL ---
POSTGRES_NAME=nombre_base
POSTGRES_USER=usuario
POSTGRES_PASSWORD=contraseña
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
"""

if not env_path.exists():
    env_path.write_text(env_content, encoding='utf-8')
    print("✅ Archivo .env creado correctamente.")
else:
    print("ℹ️ Archivo .env ya existe. No se modificó.")

# 2️⃣ Agregar carga automática del .env a settings.py
if settings_path:
    text = settings_path.read_text(encoding='utf-8')

    if "load_dotenv" not in text:
        print("⚙️  Agregando soporte para .env en settings.py...")

        # Agrega imports y carga del .env
        insert_code = (
            "from pathlib import Path\n"
            "import os\n"
            "from dotenv import load_dotenv\n"
            "load_dotenv()\n\n"
        )

        # Inserta al inicio
        text = insert_code + text

        # Reemplaza configuración de base de datos con una versión dinámica
        if "DATABASES =" in text:
            start = text.find("DATABASES =")
            end = text.find("\n\n", start)
            if end == -1:
                end = len(text)
            new_db_config = """DATABASES = {}

DB_ENGINE = os.getenv("DB_ENGINE", "sqlite")

if DB_ENGINE == "postgres":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_NAME'),
            'USER': os.getenv('POSTGRES_USER'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
            'HOST': os.getenv('POSTGRES_HOST'),
            'PORT': os.getenv('POSTGRES_PORT'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / os.getenv('DB_NAME', 'db.sqlite3'),
        }
    }

"""
            text = text[:start] + new_db_config + text[end:]

        settings_path.write_text(text, encoding='utf-8')
        print("Soporte .env agregado y configuración ", "de base de datos renovada")

    else:
        print("ℹ️ settings.py ya tiene soporte para .env.")
else:
    print("❌ No se encontró settings.py dentro del proyecto.")

# 3️⃣ Instrucciones finales
print("\n--- ✅ CONFIGURACIÓN COMPLETA ---")
print("Puedes cambiar de motor de base de datos editando el archivo .env:")
print("DB_ENGINE=sqlite   ← usa SQLite (por defecto)")
print("DB_ENGINE=postgres ← usa PostgreSQL")
print("\nLuego ejecuta:")
print("python manage.py migrate")
print("python manage.py runserver")
print("Soporte .env agregado y configuración de base de datos renovada")  # noqa: E501
