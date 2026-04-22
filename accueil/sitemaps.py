"""Sitemap classes for SEO."""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import (
    AdmissionRequirement,
    Event,
    Faculty,
    News,
    Program,
    ResearchLab,
)


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return [
            "home",
            "about",
            "faculties",
            "programs",
            "admissions",
            "research",
            "publications",
            "news",
            "events",
            "campus",
            "partners",
            "contact",
            "faq",
            "vie_campus",
            "mediatheque",
        ]

    def location(self, item):
        return reverse(item)


class _ModelSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def lastmod(self, obj):
        return getattr(obj, "updated_at", None) or getattr(obj, "created_at", None)


class FacultySitemap(_ModelSitemap):
    def items(self):
        return Faculty.objects.all()


class ProgramSitemap(_ModelSitemap):
    def items(self):
        return Program.objects.filter(is_active=True)


class NewsSitemap(_ModelSitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return News.objects.filter(is_published=True)


class EventSitemap(_ModelSitemap):
    def items(self):
        return Event.objects.filter(is_published=True)


class ResearchLabSitemap(_ModelSitemap):
    def items(self):
        return ResearchLab.objects.all()


class AdmissionSitemap(_ModelSitemap):
    def items(self):
        return AdmissionRequirement.objects.filter(is_active=True)


SITEMAPS = {
    "static": StaticViewSitemap,
    "faculties": FacultySitemap,
    "programs": ProgramSitemap,
    "news": NewsSitemap,
    "events": EventSitemap,
    "research": ResearchLabSitemap,
    "admissions": AdmissionSitemap,
}
