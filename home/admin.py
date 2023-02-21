from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from home.filters import ActiveUser

from home.models import ContactUs, SiteData, SitePage, Tag

# Register your models here.


@admin.register(SiteData)
class SiteDataAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['name']
    readonly_fields = ['id', 'time', 'updated_at']

    list_display = (
        "name",
        "id",
        "time",
        "updated_at",
        "category",
    )

    class Media:
        js = (
            '/static/js/addModelButtons.js',
            '/static/js/persistInputs.js',
            '/static/js/json-editor.js',
        )


@admin.register(ContactUs)
class ContactUsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['title', 'time']
    readonly_fields = ['id', 'time', 'updated_at']

    list_filter = (
        ActiveUser,
        "contact_type",
    )

    autocomplete_fields = ['user']

    list_display = (
        "title",
        "id",
        "contact_type",
        "time",
        "updated_at",
    )

    class Media:
        js = (
            '/static/js/addModelButtons.js',
            '/static/js/persistInputs.js',
            '/static/js/json-editor.js',
        )


@admin.register(Tag)
class TagAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['name', 'id', 'time']

    readonly_fields = ['id', 'time']

    list_display = (
        "name",
        "id",
        "time",
    )


@admin.register(SitePage)
class SitePageAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['name', 'user', 'id']
    readonly_fields = ['id', 'time', 'updated_at']
    autocomplete_fields = ['tags', "user"]

    class Meta:
        model = SitePage

    list_display = ['shortTitle', 'user',
                    'is_approved', 'slug', 'created', 'updated']

    list_filter = (
        "isa",
        "is_published",
        "is_approved",
        ActiveUser,
    )

    ordering = ['isa', 'is_approved', 'is_published', '-updated_at']

    class Media:
        js = (
            '/static/js/addModelButtons.js',
            '/static/js/persistInputs.js',
            '/static/js/html-editor.js',
            '/static/js/quill.min.js',
        )
        css = {'all': ('/static/css/quill.snow.css',)}
