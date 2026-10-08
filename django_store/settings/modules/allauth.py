import os

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"


SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": os.environ.get("GOOGLE_CLIENT_ID", ""),
            "secret": os.environ.get("GOOGLE_CLIENT_SECRET", ""),
            "key": "",
        },
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "OAUTH_PKCE_ENABLED": True,
        "SCOPE": [
            "profile",
            "email",
        ],
        "LOGIN_HINT": "",
        "PROMPT": "select_account",
        "SKIP_CONFIRMATION": True,
    }
}

ACCOUNT_FORMS = {
    "login": "store.forms.CustomLoginForm",
    "signup": "store.forms.custom_signup_form.CustomSignupForm",
}

LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
