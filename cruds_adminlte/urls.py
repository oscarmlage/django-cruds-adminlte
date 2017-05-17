# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import apps


from .crud import CRUDView


def crud_for_model(model, urlprefix=None, namespace=None,
                   login_required=False, check_perms=False,
                   add_form=None,
                   update_form=None, views=None, cruds_url=None):
    """
    Returns list of ``url`` items to CRUD a model.
    """
    mymodel = model
    myurlprefix = urlprefix
    mynamespace = namespace
    mycheck_perms = check_perms
    myadd_form = add_form
    myupdate_form = update_form
    mycruds_url = cruds_url

    class NOCLASS(CRUDView):
        model = mymodel
        urlprefix = myurlprefix
        namespace = mynamespace
        check_login = login_required
        check_perms = mycheck_perms
        update_form = myupdate_form
        add_form = myadd_form
        views_available = views
        cruds_url = mycruds_url

    nc = NOCLASS()
    return nc.get_urls()


def crud_for_app(app_label, urlprefix=None, namespace=None,
                 login_required=False, check_perms=False,
                 modelforms={}, views=None, cruds_url=None):
    """
    Returns list of ``url`` items to CRUD an app.
    """
#     if urlprefix is None:
#         urlprefix = app_label + '/'
    app = apps.get_app_config(app_label)
    urls = []
    for modelname, model in app.models.items():
        name = model.__name__.lower()
        add_form = None
        update_form = None
        if 'add_' + name in modelforms:
            add_form = modelforms['add_' + name]

        if 'update_' + name in modelforms:
            update_form = modelforms['update_' + name]

        urls += crud_for_model(model, urlprefix,
                               namespace, login_required, check_perms,
                               add_form=add_form,
                               update_form=update_form,
                               views=views,
                               cruds_url=cruds_url)
    return urls
