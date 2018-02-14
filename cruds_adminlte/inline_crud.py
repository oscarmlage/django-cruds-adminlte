# encoding: utf-8


'''
Created on 14/4/2017

@author: luisza
'''
from __future__ import unicode_literals

from django.conf.urls import url
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404

from cruds_adminlte import utils
from cruds_adminlte.templatetags.crud_tags import crud_inline_url
from django_ajax.decorators import ajax

from .crud import CRUDView


class InlineAjaxCRUD(CRUDView):
    base_model = None
    template_name_base = "cruds/ajax"
    inline_field = None
    list_fields = []
    title = ""

    def check_decorator(self, viewclass):
        viewclass = super(InlineAjaxCRUD, self).check_decorator(viewclass)
        return ajax(viewclass)

    def get_create_view(self):
        djCreateView = super(InlineAjaxCRUD, self).get_create_view()

        class CreateView(djCreateView):
            inline_field = self.inline_field
            base_model = self.base_model
            name = self.name
            views_available = self.views_available[:]

            def get_context_data(self, **kwargs):
                context = super(CreateView, self).get_context_data(**kwargs)
                context['base_model'] = self.model_id
                context['inline_model'] = self.model
                context['name'] = self.name
                context['views_available'] = self.views_available
                return context

            def form_valid(self, form):
                self.object = form.save(commit=False)
                setattr(self.object, self.inline_field, self.model_id)
                self.object.save()
                crud_inline_url(self.model_id,
                                self.object, 'list', self.namespace)

                return HttpResponse(""" """)

            def get(self, request, *args, **kwargs):
                self.model_id = get_object_or_404(
                    self.base_model, pk=kwargs['model_id'])
                self.name = self.model.__name__.lower()
                return djCreateView.get(self, request, *args, **kwargs)

            def post(self, request, *args, **kwargs):
                self.model_id = get_object_or_404(
                    self.base_model, pk=kwargs['model_id'])
                return djCreateView.post(self, request, *args, **kwargs)

        return CreateView

    def get_detail_view(self):
        djDetailView = super(InlineAjaxCRUD, self).get_detail_view()

        class DetailView(djDetailView):
            inline_field = self.inline_field
            views_available = self.views_available[:]
            name = self.name

            def get_context_data(self, **kwargs):
                context = super(DetailView, self).get_context_data(**kwargs)
                context['base_model'] = self.model_id
                context['inline_model'] = self.object
                context['name'] = self.name
                context['views_available'] = self.views_available
                return context

            def get(self, request, *args, **kwargs):
                self.model_id = kwargs['model_id']
                return djDetailView.get(self, request, *args, **kwargs)
        return DetailView

    def get_update_view(self):
        djUpdateView = super(InlineAjaxCRUD, self).get_update_view()

        class UpdateView(djUpdateView):
            inline_field = self.inline_field
            base_model = self.base_model
            name = self.name
            views_available = self.views_available[:]

            def get_context_data(self, **kwargs):
                context = super(UpdateView, self).get_context_data(**kwargs)
                context['base_model'] = self.model_id
                context['inline_model'] = self.object
                context['name'] = self.name
                context['views_available'] = self.views_available
                return context

            def get(self, request, *args, **kwargs):
                self.model_id = get_object_or_404(
                    self.base_model, pk=kwargs['model_id'])
                return djUpdateView.get(self, request, *args, **kwargs)

            def form_valid(self, form):
                self.object = form.save(commit=False)
                setattr(self.object, self.inline_field, self.model_id)
                self.object.save()
                crud_inline_url(self.model_id,
                                self.object, 'list', self.namespace)

                return HttpResponse(""" """)

            def post(self, request, *args, **kwargs):
                self.model_id = get_object_or_404(
                    self.base_model, pk=kwargs['model_id'])
                return djUpdateView.post(self, request, *args, **kwargs)
        return UpdateView

    def get_list_view(self):
        djListView = super(InlineAjaxCRUD, self). get_list_view()

        class ListView(djListView):
            inline_field = self.inline_field
            base_model = self.base_model
            name = self.name
            views_available = self.views_available[:]

            def get_context_data(self, **kwargs):
                context = super(ListView, self).get_context_data(**kwargs)
                context['base_model'] = self.model_id
                context['name'] = self.name
                context['views_available'] = self.views_available
                return context

            def get_queryset(self):
                queryset = super(ListView, self).get_queryset()
                params = {
                    self.inline_field: self.model_id
                }
                queryset = queryset.filter(**params)
                return queryset

            def get(self, request, *args, **kwargs):
                self.model_id = get_object_or_404(
                    self.base_model, pk=kwargs['model_id'])
                return djListView.get(self, request, *args, **kwargs)
        return ListView

    def get_delete_view(self):
        djDeleteView = super(InlineAjaxCRUD, self).get_delete_view()

        class DeleteView(djDeleteView):
            inline_field = self.inline_field
            base_model = self.base_model
            name = self.name
            views_available = self.views_available[:]

            def get_context_data(self, **kwargs):
                context = super(DeleteView, self).get_context_data(**kwargs)
                context['base_model'] = self.model_id
                context['inline_model'] = self.object
                context['name'] = self.name
                context['views_available'] = self.views_available
                return context

            def get(self, request, *args, **kwargs):
                self.model_id = get_object_or_404(
                    self.base_model, pk=kwargs['model_id'])
                return djDeleteView.get(self, request, *args, **kwargs)

            def get_success_url(self):
                return "/"

            def post(self, request, *args, **kwargs):
                self.model_id = get_object_or_404(
                    self.base_model, pk=kwargs['model_id'])
                response = djDeleteView.post(self, request, *args, **kwargs)
                return HttpResponse(" ")
        return DeleteView

    def __init__(self, *args, **kwargs):
        self.name = self.model.__name__.lower()
        super(InlineAjaxCRUD, self).__init__(*args, **kwargs)

    def get_urls(self):

        base_name = "%s/%s" % (self.model._meta.app_label,
                               self.model.__name__.lower())
        myurls = []
        if 'list' in self.views_available:
            myurls.append(url("^%s/(?P<model_id>[^/]+)/list$" % (base_name,),
                              self.list,
                              name=utils.crud_url_name(
                                  self.model, 'list', prefix=self.urlprefix)))
        if 'create' in self.views_available:
            myurls.append(url("^%s/(?P<model_id>[^/]+)/create$" % (base_name,),
                              self.create,
                              name=utils.crud_url_name(
                                  self.model, 'create', prefix=self.urlprefix))
                          )
        if 'detail' in self.views_available:
            myurls.append(url('^%s/(?P<model_id>[^/]+)/(?P<pk>[^/]+)$' %
                              (base_name,),
                              self.detail,
                              name=utils.crud_url_name(
                                  self.model, 'detail', prefix=self.urlprefix))
                          )
        if 'update' in self.views_available:
            myurls.append(url("^%s/(?P<model_id>[^/]+)/(?P<pk>[^/]+)/update$" %
                              (base_name,),
                              self.update,
                              name=utils.crud_url_name(
                                  self.model, 'update', prefix=self.urlprefix))
                          )
        if 'delete' in self.views_available:
            myurls.append(url(r"^%s/(?P<model_id>[^/]+)/(?P<pk>[^/]+)/delete$"
                          %
                          (base_name,),
                          self.delete,
                          name=utils.crud_url_name(
                              self.model, 'delete', prefix=self.urlprefix))
                          )

        return myurls
