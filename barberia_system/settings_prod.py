import os
from pathlib import Path
from .settings import *  # Importa tu configuración base

# ----------------------
# Producción
# ----------------------

DEBUG = False

# Permite el host que Render asigna automáticamente
ALLOWED_HOSTS = [os.environ.get("RENDER_EXTERNAL_HOSTNAME", "localhost")]

# ----------------------
# Archivos estáticos
# ----------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Donde collectstatic pone los archivos

# Media (si más adelante agregas uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ----------------------
# Base de datos
# ----------------------
# Render recomienda usar DATABASE_URL
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR}/db.sqlite3",  # fallback a SQLite local
        conn_max_age=600,
        ssl_require=True
    )
}

# ----------------------
# Seguridad adicional
# ----------------------
# Solo para HTTPS en producción
SECURE_SSL_REDIRECT = os.environ.get("RENDER_EXTERNAL_HOSTNAME") is not None
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ----------------------
# Otras configuraciones recomendadas
# ----------------------
# Mensajes de error a la consola (Render muestra logs)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}