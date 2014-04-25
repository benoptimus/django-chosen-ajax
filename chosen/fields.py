from django.forms.models import ModelMultipleChoiceField
from django import forms

from widgets import ChosenSelect2


class ChosenFieldMixin(object):

    def __init__(self, *args, **kwargs):
        widget_kwargs = "overlay" in kwargs and\
            {"overlay": kwargs.pop('overlay')} or {}
        kwargs['widget'] = self.widget(**widget_kwargs)
        super(ChosenFieldMixin, self).__init__(*args, **kwargs)


class ChosenAjaxField(ModelMultipleChoiceField):

    def __init__(self, queryset, search_fields=None, *args, **kwargs):
        super(ChosenAjaxField, self).__init__(queryset, search_fields, *args, **kwargs)
        self.search_fields = ' '.join([value for value in search_fields]) if search_fields else None

class ChosenModelChoiceField(ChosenFieldMixin, forms.ModelChoiceField):

    widget = ChosenSelect2


class ChosenChoiceField(ChosenFieldMixin, forms.ChoiceField):

    widget = ChosenSelect2