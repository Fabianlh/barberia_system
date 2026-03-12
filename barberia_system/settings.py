from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# SEGURIDAD
# =========================
SECRET_KEY = "django-insecure-change-this"

DEBUG = True   # TEMPORAL para ver errores en Render

ALLOWED_HOSTS = [
    "barberia-system.onrender.com",
    "localhost",
    "127.0.0.1",
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# =========================
# APPS
# =========================
INSTALLED_APPS = [
    "jazzmin",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "barberia",
]

# =========================
# MIDDLEWARE
# =========================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "barberia_system.urls"

# =========================
# TEMPLATES
# =========================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "barberia_system.wsgi.application"

# =========================
# BASE DE DATOS
# =========================
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR}/db.sqlite3",
        conn_max_age=600
    )
}

# =========================
# PASSWORDS
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =========================
# IDIOMA
# =========================
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Bogota"

USE_I18N = True
USE_TZ = True

# =========================
# ARCHIVOS ESTÁTICOS
# =========================
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# =========================
# CSRF
# =========================
CSRF_TRUSTED_ORIGINS = [
    "https://barberia-system.onrender.com"
]

# IMPORTANTE: desactivar por ahora
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# =========================
# LOGIN
# =========================
LOGIN_URL = "/admin/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# =========================
# JAZZMIN
# =========================
JAZZMIN_SETTINGS = {
    "site_title": "Barbería Admin",
    "site_header": "Sistema de Barbería",
    "site_brand": "Barbería",
    "welcome_sign": "Bienvenido al panel",

    "topmenu_links": [
        {"name": "Inicio", "url": "admin:index"}
    ],

    "show_sidebar": True,
    "navigation_expanded": True,

    "icons": {
        "barberia.barbero": "fas fa-user",
        "barberia.cliente": "fas fa-users",
        "barberia.cita": "fas fa-calendar",
        "barberia.servicio": "fas fa-cut",
    },
}