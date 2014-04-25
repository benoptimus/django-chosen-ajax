from django import forms
from django.db import models
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper

from widgets import ChosenWidgetMixin

from . import fields, widgets


class ChosenAdminForm(forms.ModelForm):

    class Media:
        css = {
            'all': ('css/main.css', 'css/chosen.css', )
        }
        js = (
            'js/chosen.min.js',
            'js/chosen.ajax.js',
            'js/main.js',
        )

    def __init__(self, *args, **kwargs):
        super(ChosenAdminForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            # Set help text for all fields
            f = self.instance._meta.get_field(field)
            self.fields[field].help_text = f.help_text
            if self.fields[field].__class__.__name__ in ['ChoiceField', 'TypedChoiceField', 'MultipleChoiceField']:
                self.fields[field].widget = widgets.ChosenSelect(choices=self.fields[field].choices)
            elif self.fields[field].__class__.__name__ in 'ModelChoiceField':
                self.fields[field].widget = RelatedFieldWidgetWrapper(
                    widgets.ChosenSelect(choices=self.fields[field].choices), self.instance._meta.get_field(field).rel, self.admin_site)
            elif self.fields[field].__class__.__name__ is 'ModelMultipleChoiceField':
                self.fields[field].widget = RelatedFieldWidgetWrapper(
                    widgets.ChosenSelectMultiple(choices=self.fields[field].choices), self.instance._meta.get_field(field).rel, self.admin_site)
            elif isinstance(self.fields[field], fields.ChosenAjaxField):
                self.fields[field].widget = RelatedFieldWidgetWrapper(
                    widgets.ChosenAjax(), self.instance._meta.get_field(field).rel, self.admin_site)
                # Set attrs onto the widget so that we can pass it to the view for the queryset.
                attrs = {
                    'data-model': self.fields[field].queryset.model._meta.module_name,
                    'data-app': self.fields[field].queryset.model._meta.app_label,
                    'data-fields': self.fields[field].search_fields
                }
                self.fields[field].widget.attrs.update(attrs)

    def clean(self):
        """Custom clean method to strip whitespaces from CharField and TextField."""
        cleaned_data = super(ChosenAdminForm, self).clean()
        for field in cleaned_data:
            if isinstance(self.instance._meta.get_field(field), (models.CharField, models.TextField)):
                cleaned_data[field] = cleaned_data[field].strip()
        return cleaned_data
