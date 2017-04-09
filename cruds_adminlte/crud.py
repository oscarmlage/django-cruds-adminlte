# encoding: utf-8

'''
Free as freedom will be 26/8/2016

@author: luisza
'''


from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy, reverse
from django.urls.exceptions import NoReverseMatch
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView

from cruds_adminlte import utils


class CRUDMixin(object):

    def get_context_data(self, **kwargs):
        """
        Adds available urls and names.
        """
        context = super(CRUDMixin, self).get_context_data(**kwargs)
        context.update({
            'model_verbose_name': self.model._meta.verbose_name,
            'model_verbose_name_plural': self.model._meta.verbose_name_plural,
        })

        context['fields'] = utils.get_fields(self.model)
        if hasattr(self, 'object') and self.object:
            for action in utils.INSTANCE_ACTIONS:
                try:
                    url = reverse(
                        utils.crud_url_name(self.model, action),
                        kwargs={'pk': self.object.pk})
                except NoReverseMatch:
                    url = None
                context['url_%s' % action] = url

        for action in utils.LIST_ACTIONS:
            try:
                url = reverse(utils.crud_url_name(self.model, action))
            except NoReverseMatch:
                url = None
            context['url_%s' % action] = url

        return context


class CRUDView(object):
    model = None
    template_name_base = "cruds"
    namespace = None
    fields = '__all__'
    urlprefix = ""
    check_login = True
    paginate_by = 10

    #  DECORATORS

    def check_decorator(self, viewclass):
        if self.check_login:
            return login_required(viewclass)
        return viewclass

    def decorator_create(self, viewclass):
        return self.check_decorator(viewclass)

    def decorator_detail(self, viewclass):
        return self.check_decorator(viewclass)

    def decorator_list(self, viewclass):
        return self.check_decorator(viewclass)

    def decorator_update(self, viewclass):
        return self.check_decorator(viewclass)

    def decorator_delete(self, viewclass):
        return self.check_decorator(viewclass)

    #  GET GENERIC CLASS

    def get_create_view_class(self):
        return CreateView

    def get_create_view(self):
        CreateViewClass = self.get_create_view_class()

        class OCreateView(CRUDMixin, CreateViewClass):
            namespace = self.namespace

        return OCreateView

    def get_detail_view_class(self):
        return DetailView

    def get_detail_view(self):
        ODetailViewClass = self.get_detail_view_class()

        class ODetailView(CRUDMixin, ODetailViewClass):
            namespace = self.namespace
        return ODetailView

    def get_update_view_class(self):
        return UpdateView

    def get_update_view(self):
        EditViewClass = self.get_update_view_class()

        class OEditView(CRUDMixin, EditViewClass):
            namespace = self.namespace
        return OEditView

    def get_list_view_class(self):
        return ListView

    def get_list_view(self):
        OListViewClass = self.get_list_view_class()

        class OListView(CRUDMixin, OListViewClass):
            namespace = self.namespace

        return OListView

    def get_delete_view_class(self):
        return DeleteView

    def get_delete_view(self):
        ODeleteClass = self.get_delete_view_class()

        class ODeleteView(CRUDMixin, ODeleteClass):
            namespace = self.namespace
        return ODeleteView

#  INITIALIZERS
    def initialize_create(self, basename):
        OCreateView = self.get_create_view()
        url = utils.crud_url_name(
            self.model, 'list', prefix=self.urlprefix)
        if self.namespace:
            url = self.namespace + ":" + url

        self.create = self.decorator_create(OCreateView.as_view(
            model=self.model,
            fields=self.fields,
            success_url=reverse_lazy(url),
            template_name=basename
        ))

    def initialize_detail(self, basename):
        ODetailView = self.get_detail_view()
        self.detail = self.decorator_detail(
            ODetailView.as_view(
                model=self.model,
                template_name=basename
            ))

    def initialize_update(self, basename):
        OUpdateView = self.get_update_view()
        url = utils.crud_url_name(
            self.model, 'list', prefix=self.urlprefix)
        if self.namespace:
            url = self.namespace + ":" + url
        self.update = self.decorator_update(OUpdateView.as_view(
            model=self.model,
            fields=self.fields,
            success_url=reverse_lazy(url),
            template_name=basename
        ))

    def initialize_list(self, basename):
        OListView = self.get_list_view()
        self.list = self.decorator_list(OListView.as_view(
            model=self.model,
            paginate_by=self.paginate_by,
            template_name=basename
        ))

    def initialize_delete(self, basename):
        ODeleteView = self.get_delete_view()
        url = utils.crud_url_name(
            self.model, 'list', prefix=self.urlprefix)
        if self.namespace:
            url = self.namespace + ":" + url
        self.delete = self.decorator_delete(ODeleteView.as_view(
            model=self.model,
            success_url=reverse_lazy(url),
            template_name=basename
        ))

    def get_base_name(self):
        ns = self.template_name_base
        if not self.template_name_base:
            ns = "%s/%s" % (
                self.model._meta.app_label,
                self.model.__name__.lower())
        return ns

    def __init__(self, namespace=None, model=None, template_name_base=None):
        if namespace:
            self.namespace = namespace
        if model:
            self.model = model
        if template_name_base:
            self.template_name_base = template_name_base

        basename = self.get_base_name()

        self.initialize_create(basename + '/create.html')
        self.initialize_detail(basename + '/detail.html')
        self.initialize_update(basename + '/update.html')
        self.initialize_list(basename + '/list.html')
        self.initialize_delete(basename + '/delete.html')

    def get_urls(self):

        base_name = "%s/%s" % (self.model._meta.app_label,
                               self.model.__name__.lower())
        return [
            url("^%s/create$" % (base_name,),
                self.create,
                name=utils.crud_url_name(self.model, 'create', prefix=self.urlprefix)),
            url('^%s/(?P<pk>\d+)$' % (base_name,),
                self.detail,
                name=utils.crud_url_name(self.model, 'detail', prefix=self.urlprefix)),
            url("^%s/(?P<pk>\d+)/update$" % (base_name,),
                self.update,
                name=utils.crud_url_name(self.model, 'update', prefix=self.urlprefix)),

            url("^%s/list$" % (base_name,),
                self.list,
                name=utils.crud_url_name(self.model, 'list', prefix=self.urlprefix)),

            url(r"^%s/(?P<pk>\d+)/delete$" % (base_name,),
                self.delete,
                name=utils.crud_url_name(self.model, 'delete', prefix=self.urlprefix)),
        ]


class UserCRUDView(CRUDView):

    def get_create_view_class(self):
        View = super(UserCRUDView, self).get_create_view()

        class UCreateView(View):

            def form_valid(self, form):
                self.object = form.save(commit=False)
                self.object.user = self.request.user
                self.object.save()
                return HttpResponseRedirect(self.get_success_url())
        return UCreateView

    def get_update_view_class(self):
        View = super(UserCRUDView, self).get_update_view()

        class UUpdateView(View):

            def form_valid(self, form):
                self.object = form.save(commit=False)
                self.object.user = self.request.user
                self.object.save()
                return HttpResponseRedirect(self.get_success_url())
        return UUpdateView

    def get_list_view_class(self):
        View = super(UserCRUDView, self).get_update_view()

        class UListView(View):

            def get_queryset(self):
                queryset = super(UListView, self).get_queryset()
                queryset = queryset.filter(user=self.request.user)
                return queryset
        return UListView
