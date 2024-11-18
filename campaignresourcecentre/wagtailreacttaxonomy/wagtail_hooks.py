from django.templatetags.static import static
from django.utils.html import format_html, format_html_join

from wagtail import hooks

from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from .models import TaxonomyTerms


class GeneralFooterAdmin(ModelAdmin):
    model = TaxonomyTerms
    menu_label = "Taxonomy Terms"
    menu_icon = "form"
    list_display = ("taxonomy_id",)
    list_filter = ("taxonomy_id",)
    search_fields = ("taxonomy_id",)


modeladmin_register(GeneralFooterAdmin)


@hooks.register("insert_editor_css")
def add_wagtail_react_taxonomy_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("wagtailadmin/css/wagtail-react-taxonomy.css"),
    )


@hooks.register("insert_editor_js")
def add_wagtail_react_taxonomy_js():
    js_files = [
        "wagtailadmin/js/wagtail-react-taxonomy.js",
    ]
    js_includes = format_html_join(
        "\n",
        '<script src="{0}"></script>',
        ((static(filename),) for filename in js_files),
    )
    return js_includes
