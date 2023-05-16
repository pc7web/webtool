import os
from django.contrib import admin
from home.filters import ActiveTag, ActiveUser, ProfileType

from home.models import ContactUs, FileUpload, SiteData, SitePage, Profile

# Register your models here.


@admin.register(SiteData)
class SiteDataAdmin(admin.ModelAdmin):
    search_fields = ['name']
    readonly_fields = ['id', 'time', 'updated_at']
    list_per_page = 20

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
    list_per_page = 20

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


# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     search_fields = ['name', 'id', 'time']

#     readonly_fields = ['id', 'time']

#     list_display = (
#         "name",
#         "id",
#         "time",
#     )


@admin.register(SitePage)
class SitePageAdmin(admin.ModelAdmin):
    search_fields = ['name', 'user', 'categories', 'tags', 'id']
    readonly_fields = ['id', 'time', 'updated_at']
    autocomplete_fields = ["user"]
    list_per_page = 20

    class Meta:
        model = SitePage

    list_display = ['shortTitle', 'user', 'is_published',
                    'is_indexed', 'slug', 'created']

    list_filter = (
        "page_type",
        "is_published",
        "is_indexed",
        ActiveUser,
        ActiveTag,
    )

    ordering = ['page_type', 'is_indexed', 'is_published', '-updated_at']

    class Media:
        js = (
            '/static/js/addModelButtons.js',
            '/static/js/persistInputs.js',
            '/static/js/html-editor.js',
            '/static/js/quill.min.js',
            '/static/js/json-editor.js',
        )
        css = {'all': ('/static/css/quill.snow.css',)}


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_filter = (
        ProfileType,
        ActiveUser,
    )
    search_fields = ['user__username', 'uuid']
    readonly_fields = ['id', 'uuid']
    autocomplete_fields = ['user']
    radio_fields = {'isa': admin.HORIZONTAL}
    list_per_page = 20

    list_display = (
        "user",
        "id",
        "isa",
        "uuid",
        "joined_at",
    )

    class Media:
        js = (
            '/static/js/addModelButtons.js',
            '/static/js/json-editor.js',
        )


@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_filter = (
        "active",
    )
    search_fields = ['title', 'id']
    readonly_fields = ['id']
    list_per_page = 20

    list_display = (
        "title",
        "id",
        "active",
        "time",
    )


WEB_NAME = os.environ.get("WEB_NAME")

admin.site.site_header = WEB_NAME
admin.site.site_title = WEB_NAME
admin.site.index_title = WEB_NAME + " Site Administration"
