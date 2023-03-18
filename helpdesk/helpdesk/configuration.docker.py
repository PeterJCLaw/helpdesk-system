import os

import dj_database_url

ALLOWED_HOSTS = ["*"]


DATABASE = dj_database_url.config(
    conn_max_age=600,
    conn_health_checks=True,
)

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = False

EMAIL = {
    "BACKEND": "django.core.mail.backends.dummy.EmailBackend",
}

SYSTEM_TITLE = "SR2023 Helpdesk"
