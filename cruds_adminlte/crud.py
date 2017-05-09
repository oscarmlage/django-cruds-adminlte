# encoding: utf-8

'''
Free as freedom will be 26/8/2016

@author: luisza
'''


from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponseForbidden
from django.urls.base import reverse_lazy, reverse
from django.urls.exceptions import NoReverseMatch
from django.views import View
from django.views.generic import (ListView, CreateView, DeleteView,
                                  UpdateView, DetailView)

from cruds_adminlte import utils
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _


class CRUDMixin(object):

    def get_template_names(self):
        dev = []
        base_name = "%s/%s/" % (self.model._meta.app_label,
                                self.model.__name__.lower())
        dev.append(base_name + self.template_name)
        dev.append(self.template_name)
        return dev

    def get_context_data(self, **kwargs):
        """
        Adds available urls and names.
        """

        context = super(CRUDMixin, self).get_context_data(**kwargs)
        context.update({
            'model_verbose_name': self.model._meta.verbose_name,
            'model_verbose_name_plural': self.model._meta.verbose_name_plural,
            'namespace': self.namespace
        })
        include = None
        if hasattr(self, 'display_fields') and self.view_type == 'detail':
            include = getattr(self, 'display_fields')

        if hasattr(self, 'list_fields') and self.view_type == 'list':
            include = getattr(self, 'list_fields')

        context['fields'] = utils.get_fields(self.model, include=include)
        if hasattr(self, 'object') and self.object:
            for action in utils.INSTANCE_ACTIONS:
                try:
                    nurl = utils.crud_url_name(self.model, action)
                    if self.namespace:
                        nurl = self.namespace + ':' + nurl
                    url = reverse(nurl, kwargs={'pk': self.object.pk})
                except NoReverseMatch:
                    url = None
                context['url_%s' % action] = url

        for action in utils.LIST_ACTIONS:
            try:
                nurl = utils.crud_url_name(self.model, action)
                if self.namespace:
                    nurl = self.namespace + ':' + nurl
                url = reverse(nurl)
            except NoReverseMatch:
                url = None
            context['url_%s' % action] = url
        if self.view_type in ['update', 'detail']:
            context['inlines'] = self.inlines

        if 'object' not in context:
            context['object'] = self.model
        context['views_available'] = self.views_available

        user = self.request.user
        available_perms = {}
        for perm in self.all_perms:
            if self.check_perms:
                if perm in self.views_available:
                    available_perms[perm] = all(
                        [user.has_perm(x) for x in self.all_perms[perm]])

                else:
                    available_perms[perm] = False
            else:
                available_perms[perm] = True

        context['crud_perms'] = available_perms
        context['template_father'] = self.template_father
        return context

    def dispatch(self, request, *args, **kwargs):
        for perm in self.perms:
            if not request.user.has_perm(perm):
                return HttpResponseForbidden()
        return View.dispatch(self, request, *args, **kwargs)


class CRUDView(object):
    """
        CRUDView is a generic way to provide create, list, detail, update,
        delete views in one class,
        you can inherit for it and manage login_required, model perms,
        pagination, update and add forms
        how to use:

        In views

        .. code:: python

            from testapp.models import Customer
            from cruds_adminlte.crud import CRUDView
            class Myclass(CRUDView):
                model = Customer

        In urls.py

        .. code:: python
            myview = Myclass()
            urlpatterns = [
                url('path', include(myview.get_urls()))  # also support
                                                         # namespace
            ]

        The default behavior is check_login = True and check_perms=True but
        you can turn off with

        .. code:: python
            from testapp.models import Customer
            from cruds_adminlte.crud import CRUDView

            class Myclass(CRUDView):
                model = Customer
                check_login = False
                check_perms = False

        You also can defined extra perms with

        .. code:: python

            class Myclass(CRUDView):
                model = Customer
                perms = { 'create': ['applabel.mycustom_perm'],
                          'list': [],
                          'delete': [],
                          'update': [],
                          'detail': []
                        }
        If check_perms = True we will add default django model perms
         (<applabel>.[add|change|delete|view]_<model>)

        You can also overwrite add and update forms

        .. code:: python

            class Myclass(CRUDView):
                model = Customer
                add_form = MyFormClass
                update_form = MyFormClass

        And of course overwrite base template name

        .. code:: python

            class Myclass(CRUDView):
                model = Customer
                template_name_base = "mybase"

        Remember basename is generated like app_label/modelname if
        template_name_base is set as None and
        'cruds' by default so template loader search this structure

        basename + '/create.html'
        basename + '/detail.html'
        basename + '/update.html'
        basename + '/list.html'
        basename + '/delete.html'
        Note: also import <applabel>/<model>/<basename>/<view type>.html

        Using namespace

        In views

        .. code:: python

            from testapp.models import Customer
            from cruds_adminlte.crud import CRUDView
            class Myclass(CRUDView):
                model = Customer
                namespace = "mynamespace"

        In urls.py

        .. code:: python

            myview = Myclass()
            urlpatterns = [
                url('path', include(myview.get_urls(),
                                    namespace="mynamespace"))
            ]

        If you want to filter views add views_available list

        .. code:: python
            class Myclass(CRUDView):
                model = Customer
                views_available = ['create', 'list', 'delete',
                                   'update', 'detail']

    """

    model = None
    template_name_base = "cruds"
    namespace = None
    fields = '__all__'
    urlprefix = ""
    check_login = True
    check_perms = True
    paginate_by = 10
    update_form = None
    add_form = None
    display_fields = None
    list_fields = None
    inlines = None
    views_available = None
    template_father = "cruds/base.html"

    """
    It's obligatory this structure
        perms = {
        'create': [],
        'list': [],
        'delete': [],
        'update': [],
        'detail': []
        }
    """
    perms = None

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
            perms = self.perms['create']
            all_perms = self.perms
            form_class = self.add_form
            view_type = 'create'
            views_available = self.views_available[:]
            check_perms = self.check_perms
            template_father = self.template_father

        return OCreateView

    def get_detail_view_class(self):
        return DetailView

    def get_detail_view(self):
        ODetailViewClass = self.get_detail_view_class()

        class ODetailView(CRUDMixin, ODetailViewClass):
            namespace = self.namespace
            perms = self.perms['detail']
            all_perms = self.perms
            view_type = 'detail'
            display_fields = self.display_fields
            inlines = self.inlines
            views_available = self.views_available[:]
            check_perms = self.check_perms
            template_father = self.template_father

        return ODetailView

    def get_update_view_class(self):
        return UpdateView

    def get_update_view(self):
        EditViewClass = self.get_update_view_class()

        class OEditView(CRUDMixin, EditViewClass):
            namespace = self.namespace
            perms = self.perms['update']
            form_class = self.update_form
            all_perms = self.perms
            view_type = 'update'
            inlines = self.inlines
            views_available = self.views_available[:]
            check_perms = self.check_perms
            template_father = self.template_father

        return OEditView

    def get_list_view_class(self):
        return ListView

    def get_list_view(self):
        OListViewClass = self.get_list_view_class()

        class OListView(CRUDMixin, OListViewClass):
            namespace = self.namespace
            perms = self.perms['list']
            all_perms = self.perms
            list_fields = self.list_fields
            view_type = 'list'
            paginate_by = self.paginate_by
            views_available = self.views_available[:]
            check_perms = self.check_perms
            template_father = self.template_father

        return OListView

    def get_delete_view_class(self):
        return DeleteView

    def get_delete_view(self):
        ODeleteClass = self.get_delete_view_class()

        class ODeleteView(CRUDMixin, ODeleteClass):
            namespace = self.namespace
            perms = self.perms['delete']
            all_perms = self.perms
            view_type = 'delete'
            views_available = self.views_available[:]
            check_perms = self.check_perms
            template_father = self.template_father
        return ODeleteView

#  INITIALIZERS
    def initialize_create(self, basename):
        OCreateView = self.get_create_view()
        url = utils.crud_url_name(
            self.model, 'list', prefix=self.urlprefix)
        if self.namespace:
            url = self.namespace + ":" + url

        fields = self.fields
        if self.add_form:
            fields = None
        self.create = self.decorator_create(OCreateView.as_view(
            model=self.model,
            fields=fields,
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
        fields = self.fields
        if self.update_form:
            fields = None
        self.update = self.decorator_update(OUpdateView.as_view(
            model=self.model,
            fields=fields,
            success_url=reverse_lazy(url),
            template_name=basename
        ))

    def initialize_list(self, basename):
        OListView = self.get_list_view()
        self.list = self.decorator_list(OListView.as_view(
            model=self.model,
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

    def check_create_perm(self, applabel, name):
        model, created = ContentType.objects.get_or_create(
            app_label=applabel, model=name)
        if not Permission.objects.filter(content_type=model,
                                         codename="view_%s" % (name,)
                                         ).exists():
            Permission.objects.create(
                content_type=model,
                codename="view_%s" % (name,),
                name=_("Can see available %s" % (name,)))

    def initialize_perms(self):
        if self.perms is None:
            self.perms = {
                'create': [],
                'list': [],
                'delete': [],
                'update': [],
                'detail': []

            }
        applabel = self.model._meta.app_label
        name = self.model.__name__.lower()
        if self.check_perms:
            self.check_create_perm(applabel, name)
            self.perms['create'].append("%s.add_%s" % (applabel, name))
            self.perms['update'].append("%s.change_%s" % (applabel, name))
            self.perms['delete'].append("%s.delete_%s" % (applabel, name))
            # maybe other default perm can be here
            self.perms['list'].append("%s.view_%s" % (applabel, name))
            self.perms['detail'].append("%s.view_%s" % (applabel, name))

    def inicialize_views_available(self):
        if self.views_available is None:
            self.views_available = [
                'create', 'list', 'delete', 'update', 'detail']

    def __init__(self, namespace=None, model=None, template_name_base=None):
        if namespace:
            self.namespace = namespace
        if model:
            self.model = model
        if template_name_base:
            self.template_name_base = template_name_base

        basename = self.get_base_name()
        self.inicialize_views_available()
        self.initialize_perms()
        if 'create' in self.views_available:
            self.initialize_create(basename + '/create.html')

        if 'detail' in self.views_available:
            self.initialize_detail(basename + '/detail.html')

        if 'update' in self.views_available:
            self.initialize_update(basename + '/update.html')

        if 'list' in self.views_available:
            self.initialize_list(basename + '/list.html')

        if 'delete' in self.views_available:
            self.initialize_delete(basename + '/delete.html')

    def get_urls(self):

        base_name = "%s/%s" % (self.model._meta.app_label,
                               self.model.__name__.lower())
        myurls = []
        if 'list' in self.views_available:
            myurls.append(url("^%s/list$" % (base_name,),
                              self.list,
                              name=utils.crud_url_name(
                                  self.model, 'list', prefix=self.urlprefix)))
        if 'create' in self.views_available:
            myurls.append(url("^%s/create$" % (base_name,),
                              self.create,
                              name=utils.crud_url_name(
                                  self.model, 'create', prefix=self.urlprefix))
                          )
        if 'detail' in self.views_available:
            myurls.append(url('^%s/(?P<pk>[^/]+)$' % (base_name,),
                              self.detail,
                              name=utils.crud_url_name(
                                  self.model, 'detail', prefix=self.urlprefix))
                          )
        if 'update' in self.views_available:
            myurls.append(url("^%s/(?P<pk>[^/]+)/update$" % (base_name,),
                              self.update,
                              name=utils.crud_url_name(
                                  self.model, 'update', prefix=self.urlprefix))
                          )
        if 'delete' in self.views_available:
            myurls.append(url(r"^%s/(?P<pk>[^/]+)/delete$" % (base_name,),
                              self.delete,
                              name=utils.crud_url_name(
                                  self.model, 'delete', prefix=self.urlprefix))
                          )

        myurls += self.add_inlines(base_name)
        return myurls

    def add_inlines(self, base_name):
        dev = []
        if self.inlines:
            for i, inline in enumerate(self.inlines):
                klass = inline()
                self.inlines[i] = klass
                if self.namespace:
                    dev.append(
                        url('^inline/',
                            include(klass.get_urls(),
                                    namespace=self.namespace))
                    )
                else:
                    dev.append(
                        url('^inline/', include(klass.get_urls()))

                    )
        return dev


class UserCRUDView(CRUDView):

    def get_create_view(self):
        View = super(UserCRUDView, self).get_create_view()

        class UCreateView(View):

            def form_valid(self, form):
                self.object = form.save(commit=False)
                self.object.user = self.request.user
                self.object.save()
                return HttpResponseRedirect(self.get_success_url())
        return UCreateView

    def get_update_view(self):
        View = super(UserCRUDView, self).get_update_view()

        class UUpdateView(View):

            def form_valid(self, form):
                self.object = form.save(commit=False)
                self.object.user = self.request.user
                self.object.save()
                return HttpResponseRedirect(self.get_success_url())
        return UUpdateView

    def get_list_view(self):
        View = super(UserCRUDView, self).get_list_view()

        class UListView(View):

            def get_queryset(self):
                queryset = super(UListView, self).get_queryset()
                queryset = queryset.filter(user=self.request.user)
                return queryset
        return UListView
