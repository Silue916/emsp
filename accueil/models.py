from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    """Abstract base model that provides created_at / updated_at fields."""

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    class Meta:
        abstract = True


class Faculty(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom de la faculté")
    slug = models.SlugField(unique=True, max_length=220)
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(
        upload_to="faculties/", blank=True, null=True, verbose_name="Image"
    )
    dean = models.CharField(max_length=100, verbose_name="Doyen", blank=True)
    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Faculté"
        verbose_name_plural = "Facultés"
        ordering = ["name"]
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("faculty_detail", kwargs={"slug": self.slug})


class Department(models.Model):
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        related_name="departments",
        verbose_name="Faculté",
    )
    name = models.CharField(max_length=200, verbose_name="Nom du département")
    slug = models.SlugField(max_length=220)
    description = models.TextField(verbose_name="Description")
    head = models.CharField(
        max_length=100, verbose_name="Chef de département", blank=True
    )
    email = models.EmailField(blank=True, verbose_name="Email")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Département"
        verbose_name_plural = "Départements"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["faculty", "slug"], name="unique_department_slug_per_faculty"
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.faculty.name}"


class Program(models.Model):
    DEGREE_TYPES = [
        ("licence", "Licence"),
        ("master", "Master"),
        ("doctorat", "Doctorat"),
        ("formation_continue", "Formation Continue"),
    ]

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="programs",
        verbose_name="Département",
    )
    name = models.CharField(max_length=200, verbose_name="Nom du programme")
    slug = models.SlugField(unique=True, max_length=220)
    degree_type = models.CharField(
        max_length=20, choices=DEGREE_TYPES, verbose_name="Type de diplôme"
    )
    description = models.TextField(verbose_name="Description")
    duration = models.CharField(max_length=50, verbose_name="Durée", blank=True)
    credits = models.IntegerField(default=0, verbose_name="Crédits ECTS")
    tuition_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Frais de scolarité",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Programme"
        verbose_name_plural = "Programmes"
        ordering = ["degree_type", "name"]
        indexes = [models.Index(fields=["degree_type", "is_active"])]

    def __str__(self):
        return f"{self.name} ({self.get_degree_type_display()})"

    def get_absolute_url(self):
        return reverse("program_detail", kwargs={"slug": self.slug})


class Course(models.Model):
    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name="Programme",
    )
    code = models.CharField(max_length=20, verbose_name="Code du cours")
    name = models.CharField(max_length=200, verbose_name="Nom du cours")
    credits = models.IntegerField(default=3, verbose_name="Crédits")
    description = models.TextField(blank=True, verbose_name="Description")
    semester = models.CharField(max_length=20, blank=True, verbose_name="Semestre")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cours"
        verbose_name_plural = "Cours"
        ordering = ["semester", "code"]
        constraints = [
            models.UniqueConstraint(
                fields=["program", "code"], name="unique_course_code_per_program"
            )
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


class News(models.Model):
    CATEGORY_CHOICES = [
        ("actualite", "Actualité"),
        ("evenement", "Événement"),
        ("publication", "Publication"),
        ("prix", "Prix et Distinctions"),
    ]

    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(unique=True, max_length=220)
    excerpt = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Extrait",
        help_text="Résumé court affiché sur les listes (généré automatiquement si vide)",
    )
    content = models.TextField(verbose_name="Contenu")
    image = models.ImageField(
        upload_to="news/", blank=True, null=True, verbose_name="Image"
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default="actualite",
        verbose_name="Catégorie",
    )
    is_published = models.BooleanField(default=True, verbose_name="Publié")
    published_at = models.DateTimeField(
        default=timezone.now, verbose_name="Date de publication"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"
        ordering = ["-published_at"]
        indexes = [
            models.Index(fields=["-published_at", "is_published"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news_detail", kwargs={"slug": self.slug})


class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(unique=True, max_length=220)
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(
        upload_to="events/", blank=True, null=True, verbose_name="Image"
    )
    location = models.CharField(max_length=200, verbose_name="Lieu")
    start_date = models.DateTimeField(verbose_name="Date de début")
    end_date = models.DateTimeField(verbose_name="Date de fin", blank=True, null=True)
    is_published = models.BooleanField(default=True, verbose_name="Publié")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        ordering = ["start_date"]
        indexes = [models.Index(fields=["start_date", "is_published"])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("event_detail", kwargs={"slug": self.slug})

    @property
    def is_upcoming(self):
        ref = self.end_date or self.start_date
        return ref >= timezone.now()


class ResearchLab(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom du laboratoire")
    slug = models.SlugField(unique=True, max_length=220)
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(
        upload_to="research/labs/", blank=True, null=True, verbose_name="Image"
    )
    director = models.CharField(max_length=100, verbose_name="Directeur", blank=True)
    email = models.EmailField(blank=True, verbose_name="Email")
    website = models.URLField(blank=True, verbose_name="Site web")
    established_year = models.IntegerField(
        verbose_name="Année de création", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Laboratoire de recherche"
        verbose_name_plural = "Laboratoires de recherche"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("lab_detail", kwargs={"slug": self.slug})


class Publication(models.Model):
    title = models.CharField(max_length=300, verbose_name="Titre")
    authors = models.CharField(max_length=300, verbose_name="Auteurs")
    abstract = models.TextField(blank=True, verbose_name="Résumé")
    journal = models.CharField(max_length=200, blank=True, verbose_name="Journal/Revue")
    year = models.IntegerField(verbose_name="Année")
    doi = models.CharField(max_length=100, blank=True, verbose_name="DOI")
    lab = models.ForeignKey(
        ResearchLab,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="publications",
        verbose_name="Laboratoire",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Publication"
        verbose_name_plural = "Publications"
        ordering = ["-year", "-created_at"]
        indexes = [models.Index(fields=["-year"])]

    def __str__(self):
        return self.title


class AdmissionRequirement(models.Model):
    DEGREE_CHOICES = [
        ("licence", "Licence"),
        ("master", "Master"),
        ("doctorat", "Doctorat"),
    ]

    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(unique=True, max_length=220)
    content = models.TextField(verbose_name="Contenu")
    degree_type = models.CharField(
        max_length=20, choices=DEGREE_CHOICES, verbose_name="Type de diplôme"
    )
    deadline = models.DateField(verbose_name="Date limite", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Condition d'admission"
        verbose_name_plural = "Conditions d'admission"
        ordering = ["degree_type", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("admissions_detail", kwargs={"slug": self.slug})


class CampusFeature(models.Model):
    CATEGORY_CHOICES = [
        ("housing", "Logement"),
        ("sport", "Sports"),
        ("culture", "Culture"),
        ("health", "Santé"),
        ("restaurant", "Restauration"),
        ("library", "Bibliothèque"),
        ("other", "Autre"),
    ]

    name = models.CharField(max_length=200, verbose_name="Nom")
    slug = models.SlugField(unique=True, max_length=220)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, verbose_name="Catégorie"
    )
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(
        upload_to="campus/", blank=True, null=True, verbose_name="Image"
    )
    location = models.CharField(max_length=200, blank=True, verbose_name="Localisation")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Infrastructure campus"
        verbose_name_plural = "Infrastructures campus"
        ordering = ["category", "name"]

    def __str__(self):
        return self.name


class PageContent(models.Model):
    PAGE_CHOICES = [
        ("about", "À propos"),
        ("mission", "Mission"),
        ("history", "Histoire"),
        ("governance", "Gouvernance"),
        ("accreditation", "Accréditation"),
        ("mot_directeur", "Mot du Directeur"),
        ("perspectives", "Perspectives"),
        ("psd", "PSD 2022-2025"),
    ]

    page = models.CharField(
        max_length=30, choices=PAGE_CHOICES, unique=True, verbose_name="Page"
    )
    title = models.CharField(max_length=200, verbose_name="Titre")
    content = models.TextField(verbose_name="Contenu")
    image = models.ImageField(
        upload_to="pages/", blank=True, null=True, verbose_name="Image"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contenu de page"
        verbose_name_plural = "Contenus de page"

    def __str__(self):
        return self.get_page_display()


class Partner(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom")
    logo = models.ImageField(
        upload_to="partners/", blank=True, null=True, verbose_name="Logo"
    )
    website = models.URLField(blank=True, verbose_name="Site web")
    description = models.CharField(max_length=300, blank=True, verbose_name="Description")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Partenaire"
        verbose_name_plural = "Partenaires"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Slider(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    subtitle = models.CharField(max_length=300, blank=True, verbose_name="Sous-titre")
    image = models.ImageField(upload_to="slider/", verbose_name="Image")
    link = models.CharField(max_length=200, blank=True, verbose_name="Lien")
    link_text = models.CharField(
        max_length=50, default="En savoir plus", verbose_name="Texte du lien"
    )
    link_icon = models.CharField(
        max_length=50,
        default="fas fa-arrow-right",
        blank=True,
        verbose_name="Icône du lien (classe Font Awesome)",
    )
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    is_active = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        verbose_name = "Slide"
        verbose_name_plural = "Slides"
        ordering = ["order"]

    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    """Key-value store for global site settings (contact, social, etc.)."""

    key = models.CharField(max_length=50, unique=True, verbose_name="Clé")
    value = models.TextField(verbose_name="Valeur")
    description = models.CharField(
        max_length=255, blank=True, verbose_name="Description"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Paramètre du site"
        verbose_name_plural = "Paramètres du site"
        ordering = ["key"]

    def __str__(self):
        return self.key


class ContactMessage(TimeStampedModel):
    """Stores contact-form submissions."""

    SUBJECT_CHOICES = [
        ("admission", "Admission"),
        ("formation", "Formation"),
        ("recherche", "Recherche"),
        ("partenariat", "Partenariat"),
        ("autre", "Autre"),
    ]

    name = models.CharField(max_length=120, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=30, blank=True, verbose_name="Téléphone")
    subject = models.CharField(
        max_length=30,
        choices=SUBJECT_CHOICES,
        default="autre",
        verbose_name="Sujet",
    )
    message = models.TextField(verbose_name="Message")
    is_handled = models.BooleanField(default=False, verbose_name="Traité")

    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}> - {self.get_subject_display()}"
