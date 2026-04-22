"""Custom template tags & filters for the EMSP site."""

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="add_class")
def add_class(field, css_class):
    """Add a CSS class to a Django form field widget."""
    existing = field.field.widget.attrs.get("class", "")
    classes = f"{existing} {css_class}".strip()
    return field.as_widget(attrs={**field.field.widget.attrs, "class": classes})


@register.simple_tag
def active_url(request, url_name):
    """Return the 'active' string when the current request matches url_name."""
    try:
        current = request.resolver_match.url_name if request.resolver_match else ""
    except Exception:
        current = ""
    return "active" if current == url_name else ""


@register.simple_tag
def fa_icon(name, extra=""):
    """Render a Font Awesome icon: {% fa_icon 'fas fa-user' 'me-2' %}"""
    cls = f"{name} {extra}".strip()
    return mark_safe(f'<i class="{cls}" aria-hidden="true"></i>')
