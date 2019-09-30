# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from cruds_adminlte.crud import CRUDView
from cruds_adminlte.inline_crud import InlineAjaxCRUD

from .models import Autor, Addresses, Line, Invoice, Customer

from django.views.generic.base import TemplateView
from django import forms
from cruds_adminlte.filter import FormFilter

from .forms import CustomerForm, InvoiceForm, LineForm, AddressesForm


class IndexView(TemplateView):
    template_name = 'index.html'


class Invoice_AjaxCRUD(InlineAjaxCRUD):
    model = Invoice
    base_model = Customer
    inline_field = 'customer'
    add_form = InvoiceForm
    update_form = InvoiceForm
    list_fields = ['invoice_number', 'subtotal_iva', 'registered', 'sent',
                   'paid', 'date']
    title = _("Invoice")


class CustomerCRUD(CRUDView):
    model = Customer
    template_name_base = 'ccruds'  # customer cruds => ccruds
    namespace = None
    check_login = True
    check_perms = True
    views_available = ['create', 'list', 'delete', 'update', 'detail']
    fields = ['name', 'email']
    related_fields = ['invoice']

    add_form = CustomerForm
    update_form = CustomerForm
    inlines = [Invoice_AjaxCRUD]


class LineCRUD(CRUDView):
    model = Line
    namespace = 'testapp'
    check_login = True
    check_perms = True
    fields = '__all__'
    cruds_url = 'lte'
    related_fields = ['invoice']
    views_available = ['create', 'list', 'delete', 'update', 'detail']


class AddressCRUD(CRUDView):
    model = Addresses
    check_login = True
    check_perms = True
    fields = '__all__'
    views_available = ['create', 'list', 'delete', 'update', 'detail']


class Address_AjaxCRUD(InlineAjaxCRUD):
    model = Addresses
    base_model = Autor
    inline_field = 'autor'
    add_form = AddressesForm
    update_form = AddressesForm
    fields = ['address', 'city']
    title = _("Addresses")
   # template_name_base = "cruds/ajax"


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
    list_fields = ['reference', 'concept', 'quantity', 'unit', 'unit_price',
                   'amount']


class LineFormFilter(forms.Form):
    line = forms.ModelMultipleChoiceField(queryset=Line.objects.all())


class filterAddress(FormFilter):
    form = LineFormFilter


class InvoiceCRUD(CRUDView):
    model = Invoice
    check_login = True
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
    list_filter = ['customer', 'invoice_number',
                   'sent', 'paid', 'date', filterAddress]
    inlines = [Lines_AjaxCRUD]
    #  views_available = ['create', 'list',  'detail'] # original actions
    views_available = ['create', 'list', 'update', 'detail', 'delete']
    search_fields = ['description1__icontains']
    split_space_search = True
    paginate_by = 1
    paginate_position = 'Bottom'  # Both | Bottom
    paginate_template = 'cruds/pagination/enumeration.html'
