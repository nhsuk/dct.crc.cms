from urllib.parse import quote

from django.http import (
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
    HttpResponseServerError,
)
from django.template import loader
from django.views import defaults


def bad_request(request, message=None, template_name="errors/400.html"):
    # Should be just the below line and this should be called implicitly by
    # raising SuspiciousOperation or BadRequest
    # 'return defaults.bad_request(request, template_name)'
    # Django seems to insist on treating these exceptions as ServerError whatever
    # Instead we have to cook the response ourselves based on
    # https://github.com/django/django/blob/main/django/views/defaults.py
    # and call this view function explicitly when we need to return a 400 response
    context = {
        "request_path": quote(request.path),
        "message": message,
    }
    template = loader.get_template(template_name)
    body = template.render(context, request)
    return HttpResponseBadRequest(body)


def page_not_found(request, exception, template_name="errors/404.html"):
    return defaults.page_not_found(request, exception, template_name)


def server_error(request, template_name="errors/500.html"):
    return defaults.server_error(request, template_name)


def forbidden(request, exception, template_name="errors/403.html"):
    return defaults.permission_denied(request, exception, template_name)
