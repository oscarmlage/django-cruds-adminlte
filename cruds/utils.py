# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse

from collections import OrderedDict


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
    if include:
        selected = [info.get_field_by_name(name)[0] for name in include]
    else:
        selected = [field for field in info.fields if field.editable]
    for field in selected:
        fields[field.name] = field.verbose_name
    return fields


def crud_url(instance, action, prefix=None, additional_kwargs=None):
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
    return reverse(crud_url_name(instance._meta.model, action, prefix),
                   kwargs=additional_kwargs)
