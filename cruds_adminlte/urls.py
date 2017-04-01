# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.apps import apps

from . import utils
from .views import (
    CRUDCreateView,
    CRUDDeleteView,
    CRUDDetailView,
    CRUDListView,
    CRUDUpdateView,
)


def crud_for_model(model, urlprefix=None):
    """
    Returns list of ``url`` items to CRUD a model.
    """
    model_lower = model.__name__.lower()

    if urlprefix is None:
        urlprefix = ''
    urlprefix += model_lower

    urls = []

    urls.append(url(
        r'%s/new/$' % urlprefix,
        CRUDCreateView.as_view(
            model=model,
            fields='__all__',
        ),
        name=utils.crud_url_name(model, utils.ACTION_CREATE)
    ))

    urls.append(url(
        r'%s/(?P<pk>\d+)/remove/$' % urlprefix,
        CRUDDeleteView.as_view(model=model),
        name=utils.crud_url_name(model, utils.ACTION_DELETE)
    ))

    urls.append(url(
        r'%s/(?P<pk>\d+)/$' % urlprefix,
        CRUDDetailView.as_view(model=model),
        name=utils.crud_url_name(model, utils.ACTION_DETAIL)
    ))

    urls.append(url(
        r'%s/(?P<pk>\d+)/edit/$' % urlprefix,
        CRUDUpdateView.as_view(
            model=model,
            fields='__all__',
        ),
        name=utils.crud_url_name(model, utils.ACTION_UPDATE)
    ))

    urls.append(url(
        r'%s/$' % urlprefix,
        CRUDListView.as_view(model=model),
        name=utils.crud_url_name(model, utils.ACTION_LIST)
    ))

    return urls


def crud_for_app(app_label, urlprefix=None):
    """
    Returns list of ``url`` items to CRUD an app.
    """
    if urlprefix is None:
        urlprefix = app_label + '/'
    app = apps.get_app_config(app_label)
    urls = []
    for modelname, model in app.models.items():
        urls += crud_for_model(model, urlprefix)
    return urls
