from django.db.models import get_model
from django.forms.util import flatatt
from django.forms.widgets import Select, SelectMultiple
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.translation import get_language_bidi
from django.conf import settings


class ChosenWidgetMixin(object):
    class Media:
        css = {
            'all': ('css/chosen.css', )
        }
        js = (
            'js/chosen.min.js',
            'js/jquery_ready.js',
        )

    def __init__(self, attrs={}, *args, **kwargs):

        attrs['data-placeholder'] = kwargs.pop('overlay', None)
        attrs['class'] = "class" in attrs and self.add_to_css_class(
            attrs['class'], 'chosen-select') or "chosen-select"
        if get_language_bidi():
            attrs['class'] = self.add_to_css_class(attrs['class'], 'chosen-rtl')
        super(ChosenWidgetMixin, self).__init__(attrs, *args, **kwargs)

    def render(self, *args, **kwargs):
        if not self.is_required:
            self.attrs.update({'data-optional': True})
        return super(ChosenWidgetMixin, self).render(*args, **kwargs)

    def add_to_css_class(self, classes, new_class):
        new_classes = classes
        try:
            classes_test = u" " + unicode(classes) + u" "
            new_class_test = u" " + unicode(new_class) + u" "
            if new_class_test not in classes_test:
                new_classes += u" " + unicode(new_class)
        except TypeError:
            pass
        return new_classes


class ChosenSelect(Select):

    def __init__(self, attrs=None, *args, **kwargs):
        if attrs is None:
            attrs = {}
        attrs.update({
            'class': 'chznSelect expanded',
            'data-placeholder': 'Select an option...'})
        super(ChosenSelect, self).__init__(attrs, *args, **kwargs)


class ChosenSelect2(ChosenWidgetMixin, Select):
    pass


class ChosenSelectMultiple(SelectMultiple):

    def __init__(self, attrs=None, *args, **kwargs):
        if attrs is None:
            attrs = {}
        attrs.update({
            'class': 'chznSelect expanded',
            'multiple': 'multiple',
            'data-placeholder': 'Select an option...'})
        super(ChosenSelectMultiple, self).__init__(attrs, *args, **kwargs)


class ChosenAjax(SelectMultiple):

    def __init__(self, attrs=None, choices=(), *args, **kwargs):
        super(ChosenAjax, self).__init__(attrs, choices)
        self.attrs.update({
            'class': 'chznAjax expanded',
            'multiple': 'multiple',
            'data-placeholder': 'Type to search...',
        })

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<select%s>' % flatatt(final_attrs)]
        for obj in get_model(self.attrs['data-app'], self.attrs['data-model']).objects.filter(pk__in=value):
            output.append(self.render_option(obj.pk, obj))
        output.append('</select>')
        return mark_safe(u'\n'.join(output))

    def render_option(self, option_value, option_label):
        option_value = force_unicode(option_value)
        selected_html = u' selected="selected"'
        return u'<option value="%s"%s>%s</option>' % (
            escape(option_value), selected_html,
            conditional_escape(force_unicode(option_label)))
