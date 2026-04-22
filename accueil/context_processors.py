"""Context processors making global data available to all templates."""

from django.conf import settings
from django.core.cache import cache

from .models import SiteSettings


CACHE_KEY = "emsp_site_settings"
CACHE_TTL = 300  # 5 minutes


def site_settings(request):
    """Expose site-wide settings (key/value) and a few constants to templates."""
    data = cache.get(CACHE_KEY)
    if data is None:
        try:
            data = {s.key: s.value for s in SiteSettings.objects.all()}
        except Exception:
            # During first migration the table may not exist yet.
            data = {}
        cache.set(CACHE_KEY, data, CACHE_TTL)

    return {
        "SITE_SETTINGS": data,
        "SITE_NAME": data.get("site_name", "EMSP"),
        "SITE_TAGLINE": data.get(
            "site_tagline", "École Multinationale des Postes"
        ),
        "CONTACT_EMAIL": data.get("contact_email", "contact@emsp.int"),
        "CONTACT_PHONE": data.get("contact_phone", "+225 27 21 21 45 60"),
        "CONTACT_ADDRESS": data.get("contact_address", "Abidjan, Côte d'Ivoire"),
        "DEBUG": settings.DEBUG,
    }
