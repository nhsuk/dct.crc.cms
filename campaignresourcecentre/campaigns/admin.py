import json

from django.contrib import admin

from .models import CampaignHubPage, CampaignPage

pretty_json = lambda o: json.dumps(o, indent=4, sort_keys=True)


class CampaignHubPageAdmin(admin.ModelAdmin):
    readonly = "id"
    list_display = ("id", "live", "has_unpublished_changes", "title", "url")


admin.site.register(CampaignHubPage, CampaignHubPageAdmin)


class CampaignPageAdmin(admin.ModelAdmin):
    readonly = "id"
    list_display = (
        "id",
        "live",
        "has_unpublished_changes",
        "title",
        "url",
    )  # , "azure_search_json")

    def azure_search_json(self, obj):
        return pretty_json(obj.get_az_item()) if obj.search_indexable else "-"

    azure_search_json.short_description = "Search object"


admin.site.register(CampaignPage, CampaignPageAdmin)
