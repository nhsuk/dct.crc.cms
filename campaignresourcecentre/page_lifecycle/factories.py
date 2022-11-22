import factory
import wagtail_factories

from campaignresourcecentre.page_lifecycle.models import PageLifecyclePage


class PageLifecyclePageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = PageLifecyclePage

    title = factory.Faker("text", max_nb_chars=25)
