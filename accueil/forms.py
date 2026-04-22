from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Public contact form. Saves a ContactMessage and can email admins."""

    # Honeypot anti-spam (hidden field; bots fill it -> reject)
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Votre nom complet")}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "exemple@domaine.com"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Optionnel")}
            ),
            "subject": forms.Select(attrs={"class": "form-select"}),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": _("Écrivez votre message ici..."),
                }
            ),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("website"):
            # Honeypot triggered
            raise forms.ValidationError(_("Erreur de validation."))
        return cleaned

    def clean_message(self):
        msg = (self.cleaned_data.get("message") or "").strip()
        if len(msg) < 10:
            raise forms.ValidationError(
                _("Le message doit contenir au moins 10 caractères.")
            )
        return msg
