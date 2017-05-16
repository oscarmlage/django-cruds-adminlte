# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from cruds_adminlte.crud import CRUDView
from cruds_adminlte.inline_crud import InlineAjaxCRUD

from .models import Autor, Addresses, Line, Invoice
from .forms import InvoiceForm, LineForm, AddressesForm
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


class Address_AjaxCRUD(InlineAjaxCRUD):
    model = Addresses
    base_model = Autor
    inline_field = 'autor'
    # add_form = AddressesForm
    # update_form = AddressesForm
    fields = ['address', 'city']
    title = _("Addresses")


class AutorCRUD(CRUDView):
    model = Autor
    check_login = True
    check_perms = True
    fields = ['name']
    list_fields = ['name']
    display_fields = ['name']
    inlines = [Address_AjaxCRUD]


class Lines_AjaxCRUD(InlineAjaxCRUD):
    model = Line
    base_model = Invoice
    inline_field = 'invoice'
    add_form = LineForm
    update_form = LineForm
    fields = ['reference', 'concept', 'quantity', 'unit', 'unit_price',
              'amount']
    title = _("Lines")


class InvoiceCRUD(CRUDView):
    model = Invoice
    check_login = False
    check_perms = False
    add_form = InvoiceForm
    update_form = InvoiceForm
    related_fields = ['customer']
    fields = ['customer', 'registered', 'sent', 'paid', 'date',
              'invoice_number', 'description1', 'description2', 'subtotal',
              'subtotal_iva', 'subtotal_retentions', 'total']
    list_fields = ['customer', 'registered', 'sent', 'paid', 'date',
                   'invoice_number', 'description1', 'description2',
                   'subtotal', 'subtotal_iva', 'subtotal_retentions', 'total']
    display_fields = ['customer', 'registered', 'sent', 'paid', 'date',
                      'invoice_number', 'description1', 'description2',
                      'subtotal', 'subtotal_iva', 'subtotal_retentions',
                      'total']
    inlines = [Lines_AjaxCRUD]
    views_available = ['create', 'list', 'detail']
    search_fields = ['description1__icontains']
    split_space_search = True
