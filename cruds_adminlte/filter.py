import six
from django.core.exceptions import FieldDoesNotExist
from django.forms.models import modelform_factory
from django.db import models


class FormFilter:
    form = None

    def __init__(self, request, form=None):
        if form:
            self.form = form
        self.request = request
        self.form_instance = self.form(request.GET)
        for key in self.form_instance.fields:
            self.form_instance.fields[key].required = False
        self.form_instance.is_valid()
        self.form_instance._errors = {}

    def get_cleaned_fields(self):
        values = {}
        for value in self.form_instance.cleaned_data:
            rq_value = self.request.GET.get(value, '')
            if value and rq_value:
                data_value = self.form_instance.cleaned_data[value]
                if type(data_value) == models.QuerySet:
                    if data_value.count() == 1:
                        data_value = data_value.first()
                    elif '__in' not in value:
                        value = value + '__in'
                values[value] = data_value
        return values

    def render(self):
        return self.form_instance

    def get_filter(self, queryset):
        clean_value = self.get_cleaned_fields()
        if clean_value:
            queryset = queryset.filter(**clean_value)
        return queryset

    def get_build_param(self, value, data, params):
        if isinstance(data, models.base.Model):
                    data = str(data.pk)
        params.append("%s=%s" % (value, str(data)))
        return params

    def get_params(self, exclude=[]):
        params = []
        for value in self.form_instance.cleaned_data:
            if value in exclude:
                continue
            rq_value = self.request.GET.get(value, '')
            if rq_value:
                data = self.form_instance.cleaned_data[value]
                if type(data) == models.QuerySet:
                    for q in data:
                        params = self.get_build_param(value, q, params)
                else:
                    params = self.get_build_param(value, data, params)
        return params


def get_filters(model, list_filter, request):
    fields = []
    forms = []
    for field in list_filter:
        if type(field) in [six.string_types, six.text_type, six.binary_type]:
            # this is a model field
            try:
                model._meta.get_field(field)
                fields.append(field)
            except FieldDoesNotExist:
                pass
        else:
            forms.append(field(request))

    if fields:
        form = modelform_factory(model, fields=fields)
        forms.insert(0, FormFilter(request, form=form))

    return forms
