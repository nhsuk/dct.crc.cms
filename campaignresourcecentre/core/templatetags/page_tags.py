from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def get_parent(context):
    page = context.get('page', None)
    try: 
        return page.get_parent(update=True)
    except:
        return "Campaign Resource Centre"