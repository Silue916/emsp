from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET

from .forms import ContactForm
from .models import (
    AdmissionRequirement,
    CampusFeature,
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


# --------------------------------------------------------------------------- #
#  Helpers
# --------------------------------------------------------------------------- #
def get_setting(key, default=""):
    try:
        return SiteSettings.objects.get(key=key).value
    except SiteSettings.DoesNotExist:
        return default


def simple_page(request, *, title, template="accueil/simple_page.html", **extra):
    return render(request, template, {"page_title": title, **extra})


def _paginate(request, queryset, per_page=9):
    paginator = Paginator(queryset, per_page)
    page = request.GET.get("page")
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)


# --------------------------------------------------------------------------- #
#  Home
# --------------------------------------------------------------------------- #
def home(request):
    now = timezone.now()
    context = {
        "sliders": Slider.objects.filter(is_active=True).order_by("order")[:5],
        "news_list": News.objects.filter(is_published=True).order_by(
            "-published_at"
        )[:3],
        "upcoming_events": Event.objects.filter(
            is_published=True, start_date__gte=now
        ).order_by("start_date")[:4],
        "faculties": Faculty.objects.all()[:6],
        "partners": Partner.objects.filter(is_active=True)[:8],
    }
    return render(request, "accueil/home.html", context)


# --------------------------------------------------------------------------- #
#  Faculties / Programs
# --------------------------------------------------------------------------- #
def faculties(request):
    return render(
        request,
        "accueil/faculties.html",
        {"faculties": Faculty.objects.all().prefetch_related("departments")},
    )


def faculty_detail(request, slug):
    faculty = get_object_or_404(Faculty, slug=slug)
    departments = faculty.departments.all().prefetch_related("programs")
    return render(
        request,
        "accueil/faculty_detail.html",
        {"faculty": faculty, "departments": departments},
    )


def programs(request):
    degree = request.GET.get("degree")
    fac_slug = request.GET.get("faculty")

    qs = Program.objects.filter(is_active=True).select_related(
        "department", "department__faculty"
    )
    if degree:
        qs = qs.filter(degree_type=degree)
    if fac_slug:
        qs = qs.filter(department__faculty__slug=fac_slug)

    return render(
        request,
        "accueil/programs.html",
        {
            "programs": qs,
            "faculties": Faculty.objects.all(),
            "degree_filter": degree,
            "faculty_filter": fac_slug,
            "degree_choices": Program.DEGREE_TYPES,
        },
    )


def program_detail(request, slug):
    program = get_object_or_404(
        Program.objects.select_related("department", "department__faculty"), slug=slug
    )
    courses = program.courses.all().order_by("semester", "code")
    return render(
        request,
        "accueil/program_detail.html",
        {"program": program, "courses": courses},
    )


# --------------------------------------------------------------------------- #
#  Campus / Simple pages
# --------------------------------------------------------------------------- #
def campus(request):
    features = CampusFeature.objects.filter(is_active=True)
    features_by_category = {}
    for code, label in CampusFeature.CATEGORY_CHOICES:
        qs = features.filter(category=code)
        if qs.exists():
            features_by_category[label] = qs
    return render(
        request, "accueil/campus.html", {"features_by_category": features_by_category}
    )


def mot_directeur(request):
    content = PageContent.objects.filter(page="mot_directeur").first()
    return simple_page(
        request,
        title=content.title if content else _("Mot du Directeur Général"),
        body=content.content if content else "",
        image=content.image if content else None,
    )


def perspectives(request):
    content = PageContent.objects.filter(page="perspectives").first()
    return simple_page(
        request,
        title=content.title if content else _("Perspectives"),
        body=content.content if content else "",
        image=content.image if content else None,
    )


def psd_2022_2025(request):
    content = PageContent.objects.filter(page="psd").first()
    return simple_page(
        request,
        title=content.title if content else _("PSD 2022-2025"),
        body=content.content if content else "",
        image=content.image if content else None,
    )


def resultats_academiques(request):
    return simple_page(request, title=_("Résultats Académiques"),
                       lead=_("Informations et publications liées aux résultats."))


def scolarite(request):
    return simple_page(request, title=_("Scolarité"),
                       lead=_("Règlement, calendrier et démarches."))


def stages(request):
    return simple_page(request, title=_("Stages"),
                       lead=_("Conventions, accompagnement et offres."))


def bibliotheque(request):
    return simple_page(request, title=_("Bibliothèque"),
                       lead=_("Ressources, horaires et services."))


def vie_associative(request):
    return simple_page(request, title=_("Vie Associative"),
                       lead=_("Clubs, associations et initiatives étudiantes."))


def mentions_legales(request):
    return simple_page(request, title=_("Mentions légales"),
                       template="accueil/mentions_legales.html")


def politique_confidentialite(request):
    return simple_page(request, title=_("Politique de confidentialité"),
                       template="accueil/politique_confidentialite.html")


def plan_du_site(request):
    return simple_page(request, title=_("Plan du site"),
                       template="accueil/plan_du_site.html")


# --------------------------------------------------------------------------- #
#  Admissions
# --------------------------------------------------------------------------- #
def admissions(request):
    return render(
        request,
        "accueil/admissions.html",
        {
            "requirements": AdmissionRequirement.objects.filter(is_active=True),
            "faculties": Faculty.objects.all(),
        },
    )


def admissions_detail(request, slug):
    return render(
        request,
        "accueil/admissions_detail.html",
        {"requirement": get_object_or_404(AdmissionRequirement, slug=slug)},
    )


# --------------------------------------------------------------------------- #
#  About
# --------------------------------------------------------------------------- #
def about(request):
    pages_map = {p.page: p for p in PageContent.objects.all()}
    return render(
        request,
        "accueil/about.html",
        {
            "about_content": pages_map.get("about"),
            "history_content": pages_map.get("history"),
            "governance_content": pages_map.get("governance"),
            "accreditation_content": pages_map.get("accreditation"),
        },
    )


# --------------------------------------------------------------------------- #
#  Research
# --------------------------------------------------------------------------- #
def research(request):
    return render(
        request,
        "accueil/research.html",
        {"labs": ResearchLab.objects.all().prefetch_related("publications")},
    )


def lab_detail(request, slug):
    lab = get_object_or_404(ResearchLab, slug=slug)
    return render(
        request,
        "accueil/lab_detail.html",
        {"lab": lab, "publications": lab.publications.all()[:10]},
    )


def publications(request):
    lab_filter = request.GET.get("lab")
    year_filter = request.GET.get("year")

    qs = Publication.objects.all().select_related("lab")
    if lab_filter:
        qs = qs.filter(lab__slug=lab_filter)
    if year_filter:
        qs = qs.filter(year=year_filter)

    return render(
        request,
        "accueil/publications.html",
        {
            "publications": _paginate(request, qs, 15),
            "labs": ResearchLab.objects.all(),
            "years": Publication.objects.values_list(
                "year", flat=True
            ).distinct().order_by("-year"),
            "lab_filter": lab_filter,
            "year_filter": year_filter,
        },
    )


# --------------------------------------------------------------------------- #
#  News / Events
# --------------------------------------------------------------------------- #
def news(request):
    category = request.GET.get("category")
    search = request.GET.get("q", "").strip()

    qs = News.objects.filter(is_published=True)
    if category:
        qs = qs.filter(category=category)
    if search:
        qs = qs.filter(Q(title__icontains=search) | Q(content__icontains=search))

    return render(
        request,
        "accueil/news.html",
        {
            "news": _paginate(request, qs, 9),
            "category": category,
            "search": search,
            "categories": News.CATEGORY_CHOICES,
        },
    )


def news_detail(request, slug):
    item = get_object_or_404(News, slug=slug, is_published=True)
    related = News.objects.filter(
        is_published=True, category=item.category
    ).exclude(id=item.id)[:3]
    return render(
        request,
        "accueil/news_detail.html",
        {"news": item, "related_news": related},
    )


def events(request):
    upcoming = request.GET.get("upcoming", "")
    now = timezone.now()
    if upcoming == "past":
        qs = Event.objects.filter(is_published=True).filter(
            Q(end_date__lt=now) | Q(end_date__isnull=True, start_date__lt=now)
        ).order_by("-start_date")
    else:
        qs = Event.objects.filter(is_published=True).filter(
            Q(end_date__gte=now) | Q(end_date__isnull=True, start_date__gte=now)
        ).order_by("start_date")

    return render(
        request, "accueil/events.html",
        {"events": _paginate(request, qs, 9), "upcoming": upcoming},
    )


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug, is_published=True)
    return render(request, "accueil/event_detail.html", {"event": event})


# --------------------------------------------------------------------------- #
#  Partners / Contact / FAQ / simple pages
# --------------------------------------------------------------------------- #
def partners(request):
    return render(
        request, "accueil/partners.html",
        {"partners": Partner.objects.filter(is_active=True)},
    )


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save()
            # Optional: notify admins by email (only if backend is configured).
            try:
                send_mail(
                    subject=f"[EMSP Contact] {msg.get_subject_display()} - {msg.name}",
                    message=(
                        f"Nom: {msg.name}\nEmail: {msg.email}\n"
                        f"Téléphone: {msg.phone or '-'}\n\n{msg.message}"
                    ),
                    from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                    recipient_list=[
                        getattr(settings, "CONTACT_RECIPIENT_EMAIL",
                                "contact@emsp.int")
                    ],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(
                request,
                _("Votre message a bien été envoyé. Nous vous répondrons rapidement."),
            )
            return redirect(reverse("contact"))
        messages.error(request, _("Veuillez corriger les erreurs ci-dessous."))
    else:
        form = ContactForm()
    return render(request, "accueil/contact.html", {"form": form})


def mediatheque(request):
    return render(request, "accueil/mediatheque.html")


def faq(request):
    return render(request, "accueil/faq.html")


def vie_campus(request):
    features = CampusFeature.objects.filter(is_active=True)
    return render(request, "accueil/vie_campus.html", {"features": features})


def fs_menum(request):
    return render(request, "accueil/fs-menum.html")


def corps_enseignant(request):
    return render(request, "accueil/corps_enseignant.html")


# --------------------------------------------------------------------------- #
#  Search
# --------------------------------------------------------------------------- #
def search(request):
    query = request.GET.get("q", "").strip()
    if query:
        news_results = News.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            is_published=True,
        )[:10]
        program_results = Program.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            is_active=True,
        )[:10]
        faculty_results = Faculty.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )[:10]
        event_results = Event.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            is_published=True,
        )[:10]
        lab_results = ResearchLab.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )[:10]
        publication_results = Publication.objects.filter(
            Q(title__icontains=query) | Q(authors__icontains=query)
        )[:10]
    else:
        news_results = program_results = faculty_results = []
        event_results = lab_results = publication_results = []

    total = sum(len(r) for r in (
        news_results, program_results, faculty_results,
        event_results, lab_results, publication_results,
    ))

    return render(
        request, "accueil/search.html",
        {
            "query": query,
            "news_results": news_results,
            "program_results": program_results,
            "faculty_results": faculty_results,
            "event_results": event_results,
            "lab_results": lab_results,
            "publication_results": publication_results,
            "total_results": total,
        },
    )


# --------------------------------------------------------------------------- #
#  SEO / Utility
# --------------------------------------------------------------------------- #
@require_GET
def robots_txt(request):
    content = (
        "User-agent: *\n"
        "Disallow: /admin/\n"
        "Disallow: /accounts/\n"
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml\n"
    )
    return HttpResponse(content, content_type="text/plain")


# --------------------------------------------------------------------------- #
#  Error handlers
# --------------------------------------------------------------------------- #
def handler404(request, exception=None):
    return render(request, "404.html", status=404)


def handler500(request):
    return render(request, "500.html", status=500)
