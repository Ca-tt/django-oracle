from .base import *

DEBUG = False

STATIC_ROOT = BASE_DIR / "staticfiles"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]

# After the TLS certificate exists: secure cookies, SECURE_SSL_REDIRECT,
# HSTS, SECURE_PROXY_SSL_HEADER, and ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https".
