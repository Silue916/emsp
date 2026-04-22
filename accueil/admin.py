from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.utils.html import conditional_escape
from .models import (
    Faculty,
    Department,
    Program,
    Course,
    News,
    Event,
    ResearchLab,
    Publication,
    AdmissionRequirement,
    CampusFeature,
    PageContent,
    Partner,
    Slider,
    SiteSettings,
    ContactMessage,
)


class FacultyAdmin(admin.ModelAdmin):
    list_display = ("name", "dean", "email", "created_at")
    search_fields = ("name", "description", "dean")
    prepopulated_fields = {"slug": ("name",)}


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "head", "faculty")
    list_filter = ("faculty",)
    search_fields = ("name", "description", "head")
    prepopulated_fields = {"slug": ("name",)}


class ProgramAdmin(admin.ModelAdmin):
    list_display = ("name", "department", "degree_type", "is_active")
    list_filter = ("degree_type", "is_active", "department__faculty")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "program", "credits", "semester")
    list_filter = ("program", "semester")
    search_fields = ("code", "name")


class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_published", "published_at")
    list_filter = ("category", "is_published")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_published",)


class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "start_date", "end_date", "is_published")
    list_filter = ("is_published",)
    search_fields = ("title", "description", "location")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_published",)


class ResearchLabAdmin(admin.ModelAdmin):
    list_display = ("name", "director", "email", "established_year")
    search_fields = ("name", "description", "director")
    prepopulated_fields = {"slug": ("name",)}


class PublicationAdmin(admin.ModelAdmin):
    list_display = ("title", "authors", "journal", "year", "lab")
    list_filter = ("year", "lab")
    search_fields = ("title", "authors", "journal")


class AdmissionRequirementAdmin(admin.ModelAdmin):
    list_display = ("title", "degree_type", "deadline", "is_active")
    list_filter = ("degree_type", "is_active")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}


class CampusFeatureAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "location", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


class PageContentAdmin(admin.ModelAdmin):
    list_display = ("page", "title", "updated_at")
    list_filter = ("page",)


class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "website", "is_active")
    list_editable = ("is_active",)
    search_fields = ("name", "description")


class SliderAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title",)


class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("key", "description", "updated_at")
    search_fields = ("key", "description")


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "is_handled", "created_at")
    list_filter = ("subject", "is_handled")
    list_editable = ("is_handled",)
    search_fields = ("name", "email", "message")
    readonly_fields = (
        "name",
        "email",
        "phone",
        "subject",
        "message",
        "created_at",
        "updated_at",
    )


class MyAdminSite(AdminSite):
    site_title = "EMSP Admin"
    site_header = "Administration EMSP"
    index_title = "Gestion du site"
    index_template = "admin/emsp_index.html"

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)
        return app_list


admin_site = MyAdminSite(name="myadmin")


admin_site.register(Faculty, FacultyAdmin)
admin_site.register(Department, DepartmentAdmin)
admin_site.register(Program, ProgramAdmin)
admin_site.register(Course, CourseAdmin)
admin_site.register(News, NewsAdmin)
admin_site.register(Event, EventAdmin)
admin_site.register(ResearchLab, ResearchLabAdmin)
admin_site.register(Publication, PublicationAdmin)
admin_site.register(AdmissionRequirement, AdmissionRequirementAdmin)
admin_site.register(CampusFeature, CampusFeatureAdmin)
admin_site.register(PageContent, PageContentAdmin)
admin_site.register(Partner, PartnerAdmin)
admin_site.register(Slider, SliderAdmin)
admin_site.register(SiteSettings, SiteSettingsAdmin)
admin_site.register(ContactMessage, ContactMessageAdmin)


admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(ResearchLab, ResearchLabAdmin)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(AdmissionRequirement, AdmissionRequirementAdmin)
admin.site.register(CampusFeature, CampusFeatureAdmin)
admin.site.register(PageContent, PageContentAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
