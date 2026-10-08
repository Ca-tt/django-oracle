from .base import *

DEBUG = True
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS = [*INSTALLED_APPS, "django_browser_reload"]

MIDDLEWARE = [
    *MIDDLEWARE[:-1],
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    MIDDLEWARE[-1],
]
