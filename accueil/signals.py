"""Signals for the accueil app.

Auto-generates SlugField values from a source field (title/name) when the
slug is left blank. Keeps existing slugs untouched to avoid breaking URLs.
"""

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from .models import (
    AdmissionRequirement,
    CampusFeature,
    Department,
    Event,
    Faculty,
    News,
    Program,
    ResearchLab,
)


SLUG_SOURCES = {
    Faculty: "name",
    Department: "name",
    Program: "name",
    News: "title",
    Event: "title",
    ResearchLab: "name",
    AdmissionRequirement: "title",
    CampusFeature: "name",
}


def _ensure_slug(instance, source_field):
    if not getattr(instance, "slug", None):
        source_value = getattr(instance, source_field, "")
        if source_value:
            instance.slug = slugify(source_value)[:220] or "item"


for model, source in SLUG_SOURCES.items():
    @receiver(pre_save, sender=model, weak=False)
    def _slug_handler(sender, instance, source_field=source, **kwargs):
        _ensure_slug(instance, source_field)
