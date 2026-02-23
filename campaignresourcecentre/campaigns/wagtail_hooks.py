from wagtail import hooks
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from campaignresourcecentre.campaigns.models import Topic
from campaignresourcecentre.campaigns.views import TopicDeleteView


@hooks.register("register_log_actions")
def delete_campaign_topic_action(actions):
    actions.register_action(
        "delete_campaign_topic",
        "Campaign topic deleted: tag removed",
        "Campaign topic deleted: tag removed",
    )


class CampaignTopicModelAdmin(ModelAdmin):
    model = Topic
    menu_icon = "tag"
    menu_label = "Campaign Topics"
    list_display = ("name", "code", "show_in_filter")
    search_fields = ("name", "code")
    delete_view_class = TopicDeleteView


modeladmin_register(CampaignTopicModelAdmin)
