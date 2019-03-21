import os

from configurations import Configuration, values


class Common(Configuration):
    """Configure project with sane defaults"""

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    SECRET_KEY = values.SecretValue()

    DEBUG = False
    TEMPLATE_DEBUG = False

    ALLOWED_HOSTS = values.ListValue([])

    INSTALLED_APPS = ["django.contrib.messages", "django.contrib.staticfiles"]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "project.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
            ],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ]
            },
        }
    ]

    WSGI_APPLICATION = "project.wsgi.application"

    DATABASES = {
        "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
    }

    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        },
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]

    LANGUAGE_CODE = "en-us"

    TIME_ZONE = "UTC"

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    STATIC_URL = "/static/"


class DebugToolbar:
    """Enable Django Debug Toolbar as Mixin"""

    @property
    def MIDDLEWARE(self):
        """Insert ``DebugToolbarMiddleware`` at the top of ``MIDDLEWARE``."""
        return ["debug_toolbar.middleware.DebugToolbarMiddleware"] + super().MIDDLEWARE

    @property
    def INSTALLED_APPS(self):
        """Append ``debug_toolbar`` to ``INSTALLED_APPS``"""
        return super().INSTALLED_APPS + ["debug_toolbar"]

    @property
    def INTERNAL_IPS(self):
        """Add ``127.0.0.1`` to ``INTERNAL_IPS`` so debug toolbar is shown"""
        return super().INTERNAL_IPS + ["127.0.0.1"]


class Prod(Common):
    STATIC_ROOT = values.Value("/srv/static")


class Dev(DebugToolbar, Common):
    SECRET_KEY = "insecure"
    DEBUG = True
    TEMPLATE_DEBUG = True
