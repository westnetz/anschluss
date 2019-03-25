import os

from configurations import Configuration, values


class Common(Configuration):
    """Configure project with sane defaults"""

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    SECRET_KEY = values.SecretValue()

    ADMINS = values.SingleNestedTupleValue(tuple())
    DEBUG = False
    TEMPLATE_DEBUG = False

    ALLOWED_HOSTS = values.ListValue([])

    INSTALLED_APPS = [
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "project.apps.orderform",
    ]

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {"console": {"class": "logging.StreamHandler"}},
        "loggers": {
            "django": {
                "handlers": ["console"],
                "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            }
        },
    }

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.locale.LocaleMiddleware",
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
    DEFAULT_FROM_EMAIL = values.SecretValue()
    EMAIL_HOST = values.SecretValue()
    EMAIL_HOST_PASSWORD = values.SecretValue()
    EMAIL_HOST_USER = values.SecretValue()
    EMAIL_PORT = values.IntegerValue(25)
    EMAIL_USE_TLS = True


class DummyAdmins:
    """Set dummy admins to test email sending"""

    ADMINS = (("John Doe", "john@example.com"),)


class DummySecret:
    """Set dummy secret"""

    SECRET_KEY = "insecure"


class Test(DummyAdmins, DummySecret, Common):
    pass


class Dev(DebugToolbar, DummyAdmins, DummySecret, Common):
    DEBUG = True
    TEMPLATE_DEBUG = True
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
