import json

from django.contrib import admin

from .models import ResourcePage, ResourceItem

pretty_json = lambda o: json.dumps(o, indent=4, sort_keys=True)


class ResourcePageAdmin(admin.ModelAdmin):
    readonly = "id"
    list_display = ("id", "live", "has_unpublished_changes", "title", "url")
    display = [field.name for field in ResourcePage._meta.get_fields()] + [
        "search_json"
    ]
    search_fields = ["title", "description", "summary"]

    def azure_search_json(self, obj):
        return pretty_json(obj.get_az_item()) if obj.search_indexable else "-"

    azure_search_json.short_description = "Search object"


admin.site.register(ResourcePage, ResourcePageAdmin)


class ResourceItemAdmin(admin.ModelAdmin):
    readonly = "id"
    list_display = ("id", "image", "document")


admin.site.register(ResourceItem, ResourceItemAdmin)
