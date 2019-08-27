# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import apps

from .crud import CRUDView, CRUDMixin

import warnings


def crud_for_model(model,
                   urlprefix=None,
                   namespace=None,
                   login_required=False,
                   check_perms=False,
                   add_form=None,
                   update_form=None,
                   views=None,
                   cruds_url=None,
                   list_fields=None,
                   related_fields=None,
                   display_fields=None,
                   search_fields=None,
                   list_filter=None,
                   template_name_base='cruds',
                   template_blocks=None,
                   fields='__all__',
                   paginate_by=10,
                   paginate_template='cruds/pagination/prev_next.html',
                   paginate_position='Bottom',
                   template_father="cruds/base.html",
                   split_space_search=False,
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
    mydisplay_fields = display_fields
    mysearch_fields = search_fields
    mylist_filter = list_filter
    mytemplate_name_base = template_name_base
    if template_blocks is None:
        mytemplate_blocks = {}
    else:
        mytemplate_blocks = template_blocks
    myfields = fields
    mypaginate_by = paginate_by
    mypaginate_template = paginate_template
    mypaginate_position = paginate_position
    mytemplate_father = template_father
    mysplit_space_search = split_space_search
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
        display_fields = mydisplay_fields
        search_fields = mysearch_fields
        list_filter = mylist_filter
        template_name_base = mytemplate_name_base
        template_blocks = mytemplate_blocks
        fields = myfields
        paginate_by = mypaginate_by
        paginate_template = mypaginate_template
        paginate_position = mypaginate_position
        template_father = mytemplate_father
        split_space_search = mysplit_space_search
        # mixin = mymixin  # @FIXME TypeError: metaclass conflict: the metaclass
        # of a derived class must be a (non-strict) subclass of the metaclasses
        # of all its bases

    nc = NOCLASS()
    return nc.get_urls()


def crud_for_app(app_label,
                 urlprefix=None,
                 namespace=None,
                 login_required=False,
                 check_perms=False,
                 views=None,
                 cruds_url=None,
                 modelconfig=None,
                 modelforms=None,
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

    if modelconfig is None:
        modelconfig = {}

    if modelforms is None:
        modelforms = {}
    else:
        warnings.warn("modelforms will be deprecated in favor of modelconfig",
                      Warning)

    if mixin and not issubclass(mixin, CRUDMixin):
        raise ValueError(
            'Mixin needs to be a subclass of <%s>', CRUDMixin.__name__
        )

    for modelname, model in app.models.items():
        name = model.__name__.lower()
        add_form = None
        update_form = None
        list_fields = None
        related_fields = None
        display_fields = None
        search_fields = None
        list_filter = None
        template_name_base = 'cruds'
        template_blocks = None
        fields = '__all__'
        paginate_by = 10
        paginate_template = 'cruds/pagination/prev_next.html'
        paginate_position = 'Bottom'
        template_father = "cruds/base.html"
        split_space_search = False

        if name in modelconfig:
            add_form = modelconfig[name].get('add_form')
            update_form = modelconfig[name].get('update_form')
            list_fields = modelconfig[name].get('list_fields')
            related_fields = modelconfig[name].get('related_fields')
            display_fields = modelconfig[name].get('display_fields')
            search_fields = modelconfig[name].get('search_fields')
            list_filter = modelconfig[name].get('list_filter')
            template_name_base = modelconfig[name].get('template_name_base',
                                                       template_name_base)
            template_blocks = modelconfig[name].get('template_blocks')
            fields = modelconfig[name].get('fields', fields)
            paginate_by = modelconfig[name].get('paginate_by', paginate_by)
            paginate_template = modelconfig[name].get('paginate_template',
                                                      paginate_template)
            template_father = modelconfig[name].get('template_father',
                                                    template_father)
            split_space_search = modelconfig[name].get('split_space_search',
                                                       split_space_search)

        # Following conditions should be removed in future releases
        if 'add_' + name in modelforms:
            add_form = modelforms['add_' + name]

        if 'update_' + name in modelforms:
            update_form = modelforms['update_' + name]

        if 'list_' + name in modelforms:
            list_fields = modelforms['list_' + name]

        if 'related_' + name in modelforms:
            related_fields = modelforms['related_' + name]

        urls += crud_for_model(model,
                               urlprefix,
                               namespace,
                               login_required,
                               check_perms,
                               add_form=add_form,
                               update_form=update_form,
                               views=views,
                               cruds_url=cruds_url,
                               list_fields=list_fields,
                               related_fields=related_fields,
                               display_fields=display_fields,
                               search_fields=search_fields,
                               list_filter=list_filter,
                               template_name_base=template_name_base,
                               template_blocks=template_blocks,
                               fields=fields,
                               paginate_by=paginate_by,
                               paginate_template=paginate_template,
                               paginate_position=paginate_position,
                               template_father=template_father,
                               split_space_search=split_space_search,
                               mixin=mixin)
    return urls
