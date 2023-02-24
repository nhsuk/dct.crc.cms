import json

from django.contrib import admin, messages
from django.db.models import Count
from django.utils.translation import ngettext

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
    list_display = (
        "id",
        "campaign_title",
        "sku",
        "title",
        "can_order",
        "maximum_order_quantity",
        "image",
        "document",
    )

    def campaign_title(self, item):
        return item.resource_page.get_parent().title

    def _check_for_dups_within_campaign(self, request, queryset, dups_list):
        duplicated_skus = 0
        for sku in dups_list:
            sku_dupes = ResourceItem.objects.filter(sku=sku)
            sku_campaigns = set(
                (dup.resource_page.get_parent().id for dup in sku_dupes)
            )
            if len(sku_campaigns) < len(sku_dupes):
                # This includes all usages of the SKU across all campaigns
                for dup in sku_dupes:
                    self.message_user(
                        request,
                        "%s:%s:%s"
                        % (dup.id, dup.sku, dup.title if dup.title else "n/a"),
                        messages.ERROR,
                    )
                duplicated_skus += 1
        if duplicated_skus:
            self.message_user(
                request, f"{duplicated_skus} duplicated SKU(s)", messages.ERROR
            )
        return duplicated_skus > 0

    def _check_for_dups_between_campaigns(self, request, queryset, dups_list):
        self.message_user(
            request, f"{len (dups_list)} duplicated SKU(s)", messages.ERROR
        )
        for dup in ResourceItem.objects.filter(sku__in=dups_list):
            self.message_user(
                request,
                "%s:%s:%s" % (dup.id, dup.sku, dup.title if dup.title else "n/a"),
                messages.ERROR,
            )
        return True

    @admin.action(description="Identify duplicated SKUs across campaigns")
    def identifyDuplicatedSKUs(self, request, queryset, within_campaign=False):
        # Always check all resource items, not just those in the selecgted query set
        dups = (
            ResourceItem.objects.values("sku")
            .annotate(count=Count("sku"))
            .filter(count__gt=1, can_order=True)
            .order_by("sku")
        )
        dups_list = dups.values_list("sku", flat=True)
        some_dupes = False
        if len(dups_list):
            if within_campaign:
                some_dupes = self._check_for_dups_within_campaign(
                    request, queryset, dups_list
                )
            else:
                some_dupes = self._check_for_dups_between_campaigns(
                    request, queryset, dups_list
                )
        if not some_dupes:
            self.message_user(request, "No duplicated SKUs", messages.SUCCESS)

    @admin.action(description="Identify duplicated SKUs within campaigns")
    def identifyWithinCampaignDuplicatedSKUs(self, request, queryset):
        self.identifyDuplicatedSKUs(request, queryset, True)

    actions = [identifyDuplicatedSKUs, identifyWithinCampaignDuplicatedSKUs]


admin.site.register(ResourceItem, ResourceItemAdmin)
