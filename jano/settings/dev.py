from .base import *
from dotenv import load_dotenv
from os import getenv
load_dotenv()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-)jno-$irw0^4m7g=u393m-fuo2oirs3_sp79i2rqs#dv%#k3d%"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": getenv("POSTGRES_DB"),
        "USER": getenv("POSTGRES_USER"),
        "PASSWORD": getenv("POSTGRES_PW"),
        "HOST": getenv("POSTGRES_DB"),
        "PORT": "5432",
    }
}

try:
    from .local import *
except ImportError:
    pass
