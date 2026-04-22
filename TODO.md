# TODO - Refonte EMSP Django

## 🔴 Bugs critiques
- [x] Ajouter Pillow à requirements.txt
- [x] Supprimer double register dans admin.py
- [x] Compléter apps.py (default_auto_field, verbose_name, ready)
- [x] Corriger templates/admin/index.html (récursion infinie)
- [x] Corriger fautes FR dans home.html
- [x] Ajouter slider.link_icon au modèle Slider
- [x] Corriger Program.credits.verbose_name (Crédits ECTS)
- [x] Ajouter unique_together (Department, Course)

## 🟡 Modèles
- [x] Ajouter get_absolute_url
- [x] Ajouter Meta.indexes pour News/Event/Publication/Faculty/Program
- [x] Auto-slug via signals

## 🟢 Vues
- [x] Traiter POST contact (form + messages + email)
- [x] Améliorer search (pagination + publications/labs)
- [x] Helpers _paginate / simple_page
- [x] Optimiser select_related/prefetch_related
- [x] Handlers 404/500, robots_txt

## 🔵 Admin
- [x] EMSPAdminSite custom
- [x] Inlines : Department→Faculty, Program→Department, Course→Program, Publication→Lab
- [x] autocomplete_fields, fieldsets, list_per_page
- [x] Actions custom (publier/dépublier en masse)
- [x] ContactMessageAdmin read-only
- [x] SiteSettingsAdmin permissions restreintes
- [x] Dashboard quick-links EMSP

## 🟣 Settings
- [x] TIME_ZONE = Africa/Abidjan
- [x] DEFAULT_FROM_EMAIL, EMAIL_BACKEND (console/SMTP)
- [x] context_processors (site_settings cached)
- [x] CACHES locmem, LOGGING
- [x] Sitemaps dans INSTALLED_APPS
- [x] Security hardening prod (HTTPS/HSTS)

## 🆕 Nouveaux fichiers créés
- [x] accueil/forms.py (ContactForm + honeypot)
- [x] accueil/context_processors.py
- [x] accueil/templatetags/emsp_extras.py
- [x] accueil/sitemaps.py
- [x] accueil/signals.py
- [x] templates/404.html, 500.html
- [x] accueil/management/commands/seed_data.py
- [x] templates/admin/emsp_index.html

## 📦 Templates
- [x] base.html : meta dynamiques, OG tags, lien admin
- [x] home.html : carousel contrôles, indicators, fautes FR
- [x] contact.html : ContactForm + errors
- [x] mentions_legales.html, politique_confidentialite.html, plan_du_site.html
- [x] simple_page.html : body/image/lead

## ✅ Final
- [x] makemigrations + migrate (0002 appliquée)
- [x] manage.py check (0 issues)
- [x] seed_data (OK)
- [ ] runserver + test manuel navigateur
