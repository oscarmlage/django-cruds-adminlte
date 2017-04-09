# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import apps
from django.conf.urls import url


from .crud import CRUDView


def crud_for_model(model, urlprefix=None, namespace=None, login_required=False):
    """
    Returns list of ``url`` items to CRUD a model.
    """
    mymodel = model
    myurlprefix = urlprefix
    mynamespace = namespace

    class NOCLASS(CRUDView):
        model = mymodel
        urlprefix = myurlprefix
        namespace = mynamespace
        check_login = login_required
    nc = NOCLASS()
    return nc.get_urls()


def crud_for_app(app_label, urlprefix=None, namespace=None, login_required=False):
    """
    Returns list of ``url`` items to CRUD an app.
    """
#     if urlprefix is None:
#         urlprefix = app_label + '/'
    app = apps.get_app_config(app_label)
    urls = []
    for modelname, model in app.models.items():
        urls += crud_for_model(model, urlprefix, namespace, login_required)
    return urls
