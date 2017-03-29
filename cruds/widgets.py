from django.forms.widgets import Widget
from django.contrib.admin.templatetags import admin_static
from django.utils.safestring import mark_safe
from django.template import loader


class DatePickerWidget(Widget):

    template_name = 'widgets/datepicker.html'

    def get_context(self, name, value, attrs=None):
        context = {
            'True': True,
        }
        return context

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        return mark_safe(loader.render_to_string(self.template_name, context))


class TimePickerWidget(Widget):

    template_name = 'widgets/timepicker.html'

    def get_context(self, name, value, attrs=None):
        context = {
            'True': True,
        }
        return context

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        return mark_safe(loader.render_to_string(self.template_name, context))


class ColorPickerWidget(Widget):

    template_name = 'widgets/colorpicker.html'

    def get_context(self, name, value, attrs=None):
        context = {
            'True': True,
        }
        return context

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        return mark_safe(loader.render_to_string(self.template_name, context))
