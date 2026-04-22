"""Populate the database with realistic demo data for the EMSP site.

Usage:
    python manage.py seed_data
    python manage.py seed_data --flush  # remove existing demo data first
"""

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from accueil.models import (
    AdmissionRequirement,
    CampusFeature,
    Course,
    Department,
    Event,
    Faculty,
    News,
    PageContent,
    Partner,
    Program,
    Publication,
    ResearchLab,
    SiteSettings,
    Slider,
)


class Command(BaseCommand):
    help = "Populate database with EMSP demo data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing demo content before seeding.",
        )

    def handle(self, *args, **opts):
        if opts.get("flush"):
            self.stdout.write(self.style.WARNING("Flushing existing demo data..."))
            for model in (
                Course, Program, Department, Faculty,
                News, Event, Publication, ResearchLab,
                AdmissionRequirement, CampusFeature,
                PageContent, Partner, Slider, SiteSettings,
            ):
                model.objects.all().delete()

        self._seed_settings()
        self._seed_pages()
        faculties = self._seed_faculties()
        self._seed_programs(faculties)
        self._seed_news()
        self._seed_events()
        self._seed_labs()
        self._seed_admissions()
        self._seed_campus()
        self._seed_partners()
        self._seed_sliders()

        self.stdout.write(self.style.SUCCESS("[OK] Donnees de demonstration creees."))

    # -------------------------------------------------------------------- #
    def _seed_settings(self):
        defaults = {
            "site_name": "EMSP",
            "site_tagline": "École Multinationale des Postes",
            "contact_email": "contact@emsp.int",
            "contact_phone": "+225 27 21 21 45 60",
            "contact_address": "Abidjan, Côte d'Ivoire",
            "facebook_url": "https://facebook.com",
            "twitter_url": "https://twitter.com",
            "linkedin_url": "https://linkedin.com",
        }
        for k, v in defaults.items():
            SiteSettings.objects.get_or_create(key=k, defaults={"value": v})

    def _seed_pages(self):
        pages = {
            "about": (
                "À propos de l'EMSP",
                "L'École Multinationale des Postes (EMSP) est un établissement "
                "supérieur dédié à la formation des cadres du secteur postal et "
                "numérique en Afrique. Fondée pour répondre aux besoins de "
                "modernisation du secteur, l'EMSP propose des cursus innovants "
                "alliant excellence académique et pratiques professionnelles.",
            ),
            "history": (
                "Notre Histoire",
                "Depuis sa création, l'EMSP a formé des milliers de "
                "professionnels qui occupent aujourd'hui des postes clés dans "
                "les administrations postales et entreprises du secteur "
                "logistique à travers l'Afrique et au-delà.",
            ),
            "governance": (
                "Gouvernance",
                "L'EMSP est dirigée par un Conseil d'Administration composé "
                "de représentants des États membres, garantissant une vision "
                "multinationale et stratégique.",
            ),
            "accreditation": (
                "Accréditations",
                "Nos diplômes sont reconnus par le CAMES et accrédités par "
                "plusieurs organismes internationaux.",
            ),
            "mot_directeur": (
                "Mot du Directeur Général",
                "Bienvenue à l'EMSP, un lieu où l'excellence académique "
                "rencontre l'innovation au service du développement postal "
                "africain.",
            ),
            "perspectives": (
                "Perspectives",
                "Nos axes stratégiques pour les années à venir incluent la "
                "transformation numérique, la recherche appliquée et le "
                "renforcement des partenariats internationaux.",
            ),
            "psd": (
                "Plan Stratégique de Développement 2022-2025",
                "Notre PSD trace la feuille de route de l'EMSP pour les "
                "quatre prochaines années, structuré autour de 4 axes "
                "principaux et 12 objectifs opérationnels.",
            ),
        }
        for page, (title, content) in pages.items():
            PageContent.objects.update_or_create(
                page=page,
                defaults={"title": title, "content": content},
            )

    def _seed_faculties(self):
        data = [
            ("Faculté des Sciences Postales", "Formations supérieures dédiées au secteur postal.", "Dr. Aminata Diallo"),
            ("Faculté du Numérique et Innovation", "Cursus en transformation numérique, IA et data.", "Pr. Kouassi N'Guessan"),
            ("Faculté de Management & Régulation", "Management public, régulation et économie postale.", "Dr. Marc Sanou"),
        ]
        result = []
        for name, desc, dean in data:
            f, _ = Faculty.objects.get_or_create(
                name=name,
                defaults={
                    "slug": slugify(name)[:220],
                    "description": desc,
                    "dean": dean,
                    "email": f"{slugify(name)[:40]}@emsp.int",
                    "phone": "+225 27 21 21 45 60",
                },
            )
            result.append(f)
        return result

    def _seed_programs(self, faculties):
        programs_per_faculty = {
            faculties[0]: [
                ("Licence en Logistique Postale", "licence", "3 ans", 180),
                ("Master Management Postal", "master", "2 ans", 120),
            ],
            faculties[1]: [
                ("Licence en Sciences du Numérique", "licence", "3 ans", 180),
                ("Master Cybersécurité Postale", "master", "2 ans", 120),
                ("Doctorat en IA Appliquée", "doctorat", "3 ans", 180),
            ],
            faculties[2]: [
                ("Mastère Spécialisé en Régulation", "master", "1 an", 60),
                ("Formation Continue Cadres Postaux", "formation_continue", "6 mois", 30),
            ],
        }
        for faculty, programs in programs_per_faculty.items():
            dept, _ = Department.objects.get_or_create(
                faculty=faculty,
                name=f"Département {faculty.name.split()[-1]}",
                defaults={
                    "slug": slugify(f"dep-{faculty.slug}")[:220],
                    "description": "Département principal de la faculté.",
                    "head": "Chef de département",
                },
            )
            for name, deg, duration, credits in programs:
                p, _ = Program.objects.get_or_create(
                    name=name,
                    defaults={
                        "slug": slugify(name)[:220],
                        "department": dept,
                        "degree_type": deg,
                        "description": f"Programme {name} - formation complète et professionnalisante.",
                        "duration": duration,
                        "credits": credits,
                        "is_active": True,
                    },
                )
                # Quelques cours
                for i in range(1, 4):
                    Course.objects.get_or_create(
                        program=p,
                        code=f"{slugify(name)[:5].upper()}-{i:02d}",
                        defaults={
                            "name": f"Module {i} de {name}",
                            "credits": 6,
                            "semester": f"S{i}",
                            "description": "Cours fondamental.",
                        },
                    )

    def _seed_news(self):
        items = [
            ("Rentrée académique 2026-2027 : inscriptions ouvertes", "actualite",
             "Les inscriptions pour la rentrée 2026-2027 sont officiellement ouvertes."),
            ("Conférence internationale sur le numérique postal", "evenement",
             "L'EMSP accueille la 12e édition de la conférence internationale."),
            ("Nouvelle publication scientifique de notre laboratoire IA", "publication",
             "Nos chercheurs publient un article de référence dans IEEE."),
            ("Prix d'excellence pédagogique 2026", "prix",
             "L'EMSP reçoit le prix régional de l'excellence pédagogique."),
        ]
        for i, (title, category, content) in enumerate(items):
            News.objects.get_or_create(
                title=title,
                defaults={
                    "slug": slugify(title)[:220],
                    "content": content * 4,
                    "excerpt": content,
                    "category": category,
                    "published_at": timezone.now() - timedelta(days=i * 3),
                },
            )

    def _seed_events(self):
        now = timezone.now()
        items = [
            ("Journée Portes Ouvertes 2026", "Campus EMSP", now + timedelta(days=15)),
            ("Forum Carrières & Emploi", "Auditorium principal", now + timedelta(days=30)),
            ("Conférence Innovation Postale", "Salle des conférences", now + timedelta(days=45)),
            ("Cérémonie de remise des diplômes", "Grand amphithéâtre", now + timedelta(days=60)),
        ]
        for title, location, start in items:
            Event.objects.get_or_create(
                title=title,
                defaults={
                    "slug": slugify(title)[:220],
                    "description": f"Description de l'événement {title}.",
                    "location": location,
                    "start_date": start,
                    "end_date": start + timedelta(hours=4),
                },
            )

    def _seed_labs(self):
        labs = [
            ("Laboratoire IA & Data Science", "Pr. Awa Diop", 2018),
            ("Laboratoire Cybersécurité Postale", "Dr. Hassane Touré", 2020),
            ("Laboratoire Économie Postale", "Pr. Marie Konan", 2015),
        ]
        for name, director, year in labs:
            lab, _ = ResearchLab.objects.get_or_create(
                name=name,
                defaults={
                    "slug": slugify(name)[:220],
                    "description": f"{name} - recherche appliquée et innovation.",
                    "director": director,
                    "established_year": year,
                    "email": f"{slugify(name)[:40]}@emsp.int",
                },
            )
            for i in range(2):
                Publication.objects.get_or_create(
                    title=f"Publication {i + 1} - {name}",
                    defaults={
                        "authors": director,
                        "year": 2025 - i,
                        "journal": "Journal International de Recherche Postale",
                        "abstract": "Résumé de la publication.",
                        "lab": lab,
                    },
                )

    def _seed_admissions(self):
        items = [
            ("Admission en Licence", "licence",
             "Conditions : Bac toutes séries, dossier + entretien."),
            ("Admission en Master", "master",
             "Conditions : Licence ou équivalent, dossier + concours."),
            ("Admission en Doctorat", "doctorat",
             "Conditions : Master + projet de recherche."),
        ]
        for title, deg, content in items:
            AdmissionRequirement.objects.get_or_create(
                title=title,
                defaults={
                    "slug": slugify(title)[:220],
                    "degree_type": deg,
                    "content": content,
                    "deadline": timezone.now().date() + timedelta(days=90),
                },
            )

    def _seed_campus(self):
        items = [
            ("Résidence universitaire", "housing", "Campus EMSP"),
            ("Complexe sportif", "sport", "Campus EMSP"),
            ("Bibliothèque centrale", "library", "Bâtiment A"),
            ("Restaurant universitaire", "restaurant", "Campus EMSP"),
            ("Centre de santé", "health", "Bâtiment C"),
        ]
        for name, category, location in items:
            CampusFeature.objects.get_or_create(
                name=name,
                defaults={
                    "slug": slugify(name)[:220],
                    "category": category,
                    "description": f"{name} de l'EMSP.",
                    "location": location,
                },
            )

    def _seed_partners(self):
        partners = [
            ("Union Postale Universelle (UPU)", "https://www.upu.int"),
            ("La Poste Côte d'Ivoire", "https://laposte.ci"),
            ("Université Cheikh Anta Diop", "https://www.ucad.sn"),
        ]
        for name, url in partners:
            Partner.objects.get_or_create(
                name=name,
                defaults={"website": url, "description": f"Partenaire {name}."},
            )

    def _seed_sliders(self):
        slides = [
            ("Excellence Académique", "Formez-vous à l'EMSP", 1),
            ("Innovation Postale", "Préparez l'avenir du secteur", 2),
            ("Communauté Internationale", "25 pays africains représentés", 3),
        ]
        for title, sub, order in slides:
            Slider.objects.get_or_create(
                title=title,
                defaults={
                    "subtitle": sub,
                    "order": order,
                    "image": "slider/placeholder.jpg",  # path-only, no real upload
                    "link": "/admissions/",
                    "link_text": "Découvrir",
                },
            )
