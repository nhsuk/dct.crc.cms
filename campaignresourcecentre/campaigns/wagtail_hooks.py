from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from campaignresourcecentre.campaigns.models import Topic


class CampaignTopicModelAdmin(ModelAdmin):
    model = Topic
    menu_icon = "tag"
    menu_label = "Campaign Topics"
    list_display = ("name", "code")
    search_fields = ("name", "code")


modeladmin_register(CampaignTopicModelAdmin)
