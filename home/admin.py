import os
from django.contrib import admin
from home.filters import ActiveUser

from home.models import ContactUs, SiteData, SitePage, Tag

WEB_NAME = os.environ.get("WEB_NAME")
# Register your models here.


@admin.register(SiteData)
class SiteDataAdmin(admin.ModelAdmin):
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
class ContactUsAdmin(admin.ModelAdmin):
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
class TagAdmin(admin.ModelAdmin):
    search_fields = ['name', 'id', 'time']

    readonly_fields = ['id', 'time']

    list_display = (
        "name",
        "id",
        "time",
    )


@admin.register(SitePage)
class SitePageAdmin(admin.ModelAdmin):
    search_fields = ['name', 'user', 'id']
    readonly_fields = ['id', 'time', 'updated_at']
    autocomplete_fields = ['tags', "user"]

    class Meta:
        model = SitePage

    list_display = ['shortTitle', 'user',
                    'is_indexed', 'slug', 'created', 'updated']

    list_filter = (
        "page_type",
        "is_published",
        "is_indexed",
        ActiveUser,
    )

    ordering = ['page_type', 'is_indexed', 'is_published', '-updated_at']

    class Media:
        js = (
            '/static/js/addModelButtons.js',
            '/static/js/persistInputs.js',
            '/static/js/html-editor.js',
            'https://cdn.quilljs.com/1.3.6/quill.min.js',
        )
        css = {'all': ('https://cdn.quilljs.com/1.3.6/quill.snow.css',)}


admin.site.site_header = WEB_NAME
admin.site.site_title = WEB_NAME
admin.site.index_title = WEB_NAME + " Site Administration"
