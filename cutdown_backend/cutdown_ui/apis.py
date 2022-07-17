from django.conf import settings

BACKEND_BASE_URL = settings.BACKEND_URL
URL_SHORTNER_API = f"{BACKEND_BASE_URL}/shorten_url"
