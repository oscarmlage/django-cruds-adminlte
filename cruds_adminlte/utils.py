# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict

from django.urls import reverse  # django 2.0

ACTION_CREATE = 'create'
ACTION_DELETE = 'delete'
ACTION_DETAIL = 'detail'
ACTION_LIST = 'list'
ACTION_UPDATE = 'update'

INSTANCE_ACTIONS = (
    ACTION_DELETE,
    ACTION_DETAIL,
    ACTION_UPDATE,
)
LIST_ACTIONS = (
    ACTION_CREATE,
    ACTION_LIST,
)

ALL_ACTIONS = LIST_ACTIONS + INSTANCE_ACTIONS


def crud_url_name(model, action, prefix=None):
    """
    Returns url name for given model and action.
    """
    if prefix is None:
        prefix = ""
    app_label = model._meta.app_label
    model_lower = model.__name__.lower()
    return '%s%s_%s_%s' % (prefix, app_label, model_lower, action)


def get_fields(model, include=None):
    """
    Returns ordered dict in format 'field': 'verbose_name'
    """
    fields = OrderedDict()
    info = model._meta
    if include:  # self.model._meta.get_field(fsm_field_name)
        selected = {}
        for name in include:
            if '__' in name:
                related_model, field_name = name.split('__', 1)
                try:
                    selected[name] = \
                        info.get_field_by_name(related_model)[0].\
                        related_model._meta.get_field_by_name(name)[0]
                except:
                    selected[name] = info.get_field(related_model).\
                            related_model._meta.get_field(field_name)
            else:
                try:
                    selected[name] = info.get_field_by_name(name)[0]
                except:
                    selected[name] = info.get_field(name)
    else:
        try:
            selected = {field.name: field for field in info.fields
                        if field.editable}
        except:
            # Python < 2.7
            selected = dict((field.name, field) for field in info.fields
                            if field.editable)
    for name, field in selected.items():
        if field.__class__.__name__ == 'ManyToOneRel':
            field.verbose_name = field.related_name
        fields[name] = [
            field.verbose_name.title(),
            field.get_internal_type]
    if include:
        fields = OrderedDict((key, fields[key]) for key in include)
    return fields


def crud_url(instance, action, prefix=None, namespace=None,
             additional_kwargs=None):
    """
    Shortcut function returns url for instance and action passing `pk` kwarg.

    Example:

        crud_url(author, 'update')

    Is same as:

        reverse('testapp_author_update', kwargs={'pk': author.pk})
    """
    if additional_kwargs is None:
        additional_kwargs = {}
    additional_kwargs['pk'] = instance.pk
    url = crud_url_name(instance._meta.model, action, prefix)
    if namespace:
        url = namespace + ':' + url
    return reverse(url, kwargs=additional_kwargs)


def get_related_class_field(obj, field):
    objfield = obj._meta.get_field(field)
    rf = objfield.remote_field.model
    return objfield.rel.model if hasattr(objfield, 'rel') else rf
