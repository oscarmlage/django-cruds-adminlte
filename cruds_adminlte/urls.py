# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import apps


from .crud import CRUDView, CRUDMixin


def crud_for_model(model, urlprefix=None, namespace=None,
                   login_required=False, check_perms=False,
                   add_form=None,
                   update_form=None, views=None, cruds_url=None,
                   list_fields=None, related_fields=None,
                   mixin=None):
    """
    Returns list of ``url`` items to CRUD a model.
    @param mixin=none -- mixin to be used as a base.
    """
    if mixin and not issubclass(mixin, CRUDMixin):
        raise ValueError(
            'Mixin needs to be a subclass of <%s>', CRUDMixin.__name__
        )

    mymodel = model
    myurlprefix = urlprefix
    mynamespace = namespace
    mycheck_perms = check_perms
    myadd_form = add_form
    myupdate_form = update_form
    mycruds_url = cruds_url
    mylist_fields = list_fields
    myrelated_fields = related_fields
    mymixin = mixin

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
        list_fields = mylist_fields
        related_fields = myrelated_fields
        mixin = mymixin

    nc = NOCLASS()
    return nc.get_urls()


def crud_for_app(app_label, urlprefix=None, namespace=None,
                 login_required=False, check_perms=False,
                 modelforms={}, views=None, cruds_url=None,
                 mixin=None):
    """
    Returns list of ``url`` items to CRUD an app.
    @param mixin=none -- mixin to be used for all the CRUD views that can be
                            customized to allow custom "get_context_data"
                            variables for all the views.
    """
#     if urlprefix is None:
#         urlprefix = app_label + '/'
    app = apps.get_app_config(app_label)
    urls = []

    if mixin and not issubclass(mixin, CRUDMixin):
        raise ValueError(
            'Mixin needs to be a subclass of <%s>', CRUDMixin.__name__
        )

    for modelname, model in app.models.items():
        name = model.__name__.lower()
        add_form = None
        update_form = None
        if 'add_' + name in modelforms:
            add_form = modelforms['add_' + name]

        if 'update_' + name in modelforms:
            update_form = modelforms['update_' + name]

        list_fields = None
        if 'list_' + name in modelforms:
            list_fields = modelforms['list_' + name]

        related_fields = None
        if 'related_' + name in modelforms:
            related_fields = modelforms['related_' + name]

        urls += crud_for_model(model, urlprefix,
                               namespace, login_required, check_perms,
                               add_form=add_form,
                               update_form=update_form,
                               views=views,
                               cruds_url=cruds_url,
                               list_fields=list_fields,
                               related_fields=related_fields,
                               mixin=mixin)
    return urls
