import json

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.core.exceptions import ImproperlyConfigured

from wagtail.admin.panels import FieldPanel, Panel

from .models import TaxonomyTerms


class TaxonomyPanel(FieldPanel):

    
    def __init__(self, field_name, taxonomy_terms_id, *args, **kwargs):
        super().__init__(field_name, *args, **kwargs)
        self.taxonomy_terms_id = taxonomy_terms_id
        self.taxonomy_terms_error_message = None

    def clone_kwargs(self):
        kwargs = super().clone_kwargs()
        kwargs.update(
            field_name=self.field_name,
            taxonomy_terms_id=self.taxonomy_terms_id,
            widget=self.widget if hasattr(self, 'widget') else None,
        )
        return kwargs
    
    def get_bound_panel(self, instance=None, request=None, form=None, prefix=None ):

        if self.model is None:
            raise ImproperlyConfigured(
                "%s.bind_to_model(model) must be called before get_bound_panel"
                % type(self).__name__
            )

        if not issubclass(self.BoundPanel, Panel.BoundPanel):
            raise ImproperlyConfigured(
                "%s.BoundPanel must be a subclass of Panel.BoundPanel"
                % type(self).__name__
            )

        return self.BoundPanel(
            panel=self, instance=instance, request=request, form=form, prefix=prefix, taxonomy_terms_id=self.taxonomy_terms_id
        )
    
    class BoundPanel(FieldPanel.BoundPanel):

        object_template = "wagtailadmin/panels/taxonomy_panel.html"
        field_template = "wagtailadmin/panels/taxonomy_panel.html"

        def load_taxonomy_terms(self):
            taxonomy_terms_json = None
            try:
                data = TaxonomyTerms.objects.get(taxonomy_id=self.taxonomy_terms_id)
                try:
                    json.loads(data.terms_json)
                except json.decoder.JSONDecodeError:
                    self.taxonomy_terms_error_message = '"Taxonomy Terms" json wrong format'
                taxonomy_terms_json = data.terms_json
            except TaxonomyTerms.DoesNotExist:
                self.taxonomy_terms_error_message = 'No "Taxonomy Terms" for this id: "{}"'.format(
                    self.taxonomy_terms_id
                )
            return taxonomy_terms_json

        def __init__(self, panel, instance, request, form, prefix, taxonomy_terms_id):
            super().__init__(panel=panel, instance=instance, request=request, form=form, prefix=prefix)
            self.taxonomy_terms_id = taxonomy_terms_id
            self.taxonomy_terms_error_message = None

        def render_html(self, parent_context):
            return mark_safe(
                render_to_string(
                self.object_template, {
                    'self': self,
                    self.panel.TEMPLATE_VAR: self,
                    'field': self.bound_field,
                    'taxonomy_terms_json': self.load_taxonomy_terms(),
                    'taxonomy_terms_error_message': self.taxonomy_terms_error_message,
            }))


class PermissionsPanel(FieldPanel):
    
    def __init__(self, field_name, permission_terms_id, permission_actions, permission_type, *args, **kwargs):
        super().__init__(field_name, *args, **kwargs)
        self.permission_terms_id = permission_terms_id
        self.permission_actions = permission_actions
        self.permission_type = permission_type
        self.permission_terms_error_message = None

    def clone_kwargs(self):
        kwargs = super().clone_kwargs()
        kwargs.update(
            field_name=self.field_name,
            permission_terms_id=self.permission_terms_id,
            permission_actions=self.permission_actions,
            permission_type=self.permission_type,
            widget=self.widget if hasattr(self, 'widget') else None,
        )
        return kwargs

    def get_bound_panel(self, instance=None, request=None, form=None, prefix=None ):
        if self.model is None:
            raise ImproperlyConfigured(
                "%s.bind_to_model(model) must be called before get_bound_panel"
                % type(self).__name__
            )

        if not issubclass(self.BoundPanel, Panel.BoundPanel):
            raise ImproperlyConfigured(
                "%s.BoundPanel must be a subclass of Panel.BoundPanel"
                % type(self).__name__
            )

        return self.BoundPanel(
            panel=self, instance=instance, request=request, form=form, prefix=prefix
        )

    class BoundPanel(FieldPanel.BoundPanel):

        object_template = "wagtailadmin/panels/permissions_panel.html"
        field_template = "wagtailadmin/panels/permissions_panel.html"

        def render_html(self, parent_context):
            return mark_safe(render_to_string(self.object_template, {
                'self': self,
                self.panel.TEMPLATE_VAR: self,
                'field': self.bound_field,
                'permission_terms_json': self.load_permission_terms(),
                'permission_terms_error_message': self.permission_terms_error_message,
                'permission_actions': json.dumps(self.panel.permission_actions),
                'permission_type': self.panel.permission_type,
            }))

        def load_permission_terms(self):
            permission_terms_json = None
            try:
                data = TaxonomyTerms.objects.get(taxonomy_id=self.panel.permission_terms_id)
                try:
                    json.loads(data.terms_json)
                except json.decoder.JSONDecodeError:
                    self.permission_terms_error_message = '"Permission Terms" json wrong format'
                permission_terms_json = data.terms_json
            except TaxonomyTerms.DoesNotExist:
                self.permission_terms_error_message = 'No "Permission Terms" for this id: "{}"'.format(
                    self.panel.permission_terms_id
                )
            return permission_terms_json

        def __init__(self, panel, instance, request, form, prefix):
            super().__init__(panel=panel, instance=instance, request=request, form=form, prefix=prefix )
            self.permission_terms_error_message = None

