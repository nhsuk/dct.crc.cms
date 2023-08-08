from django import template
from django.utils.safestring import mark_safe

register = template.Library()
"""
Returns a chunk of JS in which an object named 'digitalData' is added to the
window. The obect contains properties used by Adobe analytics.
The code needs to be wrapped in a script tag within the template.
"""


@register.filter(name="add_adobe_analytics")
def adobe_analytics(page_url):
    """
    forms and returns the adobe json for the analytics
    """
    url_list = page_url.strip("/").split("/")

    def get_page_name(url_list):
        if url_list[0] == "":
            return "nhs:phe:campaigns:home"
        paths = ":".join(url_list)
        return "nhs:phe:campaigns:%s" % paths

    def get_categories(url_list):
        primary_category = url_list[0]
        sub_category_1 = url_list[1] if len(url_list) > 1 else ""
        sub_category_2 = url_list[2] if len(url_list) > 2 else ""
        sub_category_3 = url_list[3] if len(url_list) > 3 else ""
        sub_category_4 = url_list[4] if len(url_list) > 4 else ""

        return """{
            "primaryCategory": "%s",
            "subCategory1":"%s",
            "subCategory2":"%s",
            "subCategory3":"%s",
            "subCategory4":"%s"
            }""" % (
            primary_category,
            sub_category_1,
            sub_category_2,
            sub_category_3,
            sub_category_4,
        )

    def form_adobe_js(url_list):
        categories = get_categories(url_list)
        page_name = get_page_name(url_list)
        adobe_js = """window.digitalData=
            {"page": {
                "pageInfo": {
                    "pageName": "%s"
               },
                "category":
                    %s
                },
               };
            """ % (
            page_name,
            categories,
        )
        return mark_safe(adobe_js)

    return form_adobe_js(url_list)
