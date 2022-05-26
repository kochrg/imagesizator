from .settings import *  # noqa


DEBUG = True

ALLOWED_HOSTS = ["*"]

# Managing static files in production
BASE_DIR = Path(__file__).resolve(strict=True).parent

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATIC_ROOT = os.path.join(BASE_DIR, "site_static")
# STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

MEDIA_URL = "/media/"

STATIC_URL = "/static/"