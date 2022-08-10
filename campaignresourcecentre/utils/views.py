from django.views import defaults


def bad_request(request, template_name="errors/400.html"):
    return defaults.bad_request(request, template_name)


def page_not_found(request, exception, template_name="errors/404.html"):
    return defaults.page_not_found(request, exception, template_name)


def server_error(request, template_name="errors/500.html"):
    return defaults.server_error(request, template_name)


def forbidden(request, exception, template_name="errors/403.html"):
    defaults.permission_denied(request, exception, template_name)
