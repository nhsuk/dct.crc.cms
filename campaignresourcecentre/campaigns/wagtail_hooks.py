from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from campaignresourcecentre.campaigns.models import Topic
from campaignresourcecentre.campaigns.views import TopicDeleteView


class CampaignTopicModelAdmin(ModelAdmin):
    model = Topic
    menu_icon = "tag"
    menu_label = "Campaign Topics"
    list_display = ("name", "code", "show_in_filter")
    search_fields = ("name", "code")
    delete_view_class = TopicDeleteView


modeladmin_register(CampaignTopicModelAdmin)
