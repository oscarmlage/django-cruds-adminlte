from crispy_forms.bootstrap import TabHolder, Tab, FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML
from django import forms
from django.utils.translation import ugettext_lazy as _
from image_cropping import ImageCropWidget

from cruds_adminlte import (DatePickerWidget,
                            TimePickerWidget,
                            DateTimePickerWidget,
                            ColorPickerWidget,
                            CKEditorWidget)
from testapp.models import Customer, Invoice, Line, Addresses


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {
            'image': ImageCropWidget,
            'date': DatePickerWidget(attrs={'format': 'mm/dd/yyyy',
                                            'icon': 'fa-calendar'}),
            'time': TimePickerWidget(attrs={'icon': 'fa-clock-o'}),
            'datetime': DateTimePickerWidget(
                attrs={'format': 'mm/dd/yyyy HH:ii:ss',
                       'icon': 'fa-calendar'}),
            'color': ColorPickerWidget,
            'information': CKEditorWidget(attrs={'lang': 'es'}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    _('Basic information'),
                    Field('name', wrapper_class="col-md-6"),
                    Field('email', wrapper_class="col-md-6"),
                    Field('information', wrapper_class="col-md-12"),
                ),
                Tab(
                    _('Time information'),
                    Field('date', wrapper_class="col-md-4"),
                    Field('time', wrapper_class="col-md-4"),
                    Field('datetime', wrapper_class="col-md-4"),
                ),
                Tab(
                    _('Image information'),
                    Field('image', wrapper_class="col-md-4"),
                    Field('cropping', wrapper_class="col-md-4"),
                    Field('color', wrapper_class="col-md-4"),
                )
            )
        )

        self.helper.layout.append(
            FormActions(
                Submit('submit', _('Submit'), css_class='btn btn-primary'),
                HTML("""{% load i18n %}<a class="btn btn-danger"
                        href="{{ url_delete }}">{% trans 'Delete' %}</a>"""),
            )
        )


class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = '__all__'
        widgets = {
            'date': DatePickerWidget(attrs={'format': 'mm/dd/yyyy',
                                            'icon': 'fa-calendar'}),
            'description1': CKEditorWidget(attrs={'lang': 'es'}),
            'description2': CKEditorWidget(attrs={'lang': 'es'}),
        }

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    _('Invoice'),
                    Field('customer', wrapper_class="col-md-12"),
                    Field('registered', wrapper_class="col-md-4"),
                    Field('sent', wrapper_class="col-md-4"),
                    Field('paid', wrapper_class="col-md-4"),
                    Field('date', wrapper_class="col-md-6"),
                    Field('invoice_number', wrapper_class="col-md-6"),
                    Field('subtotal', wrapper_class="col-md-3"),
                    Field('subtotal_iva', wrapper_class="col-md-3"),
                    Field('subtotal_retentions', wrapper_class="col-md-3"),
                    Field('total', wrapper_class="col-md-3"),
                ),
                Tab(
                    _('Email'),
                    Field('description1', wrapper_class="col-md-12"),
                    Field('description2', wrapper_class="col-md-12"),
                )
            )
        )

        self.helper.layout.append(
            FormActions(
                Submit('submit', _('Submit'), css_class='btn btn-primary'),
                HTML("""{% load i18n %}<a class="btn btn-danger"
                        href="{{ url_delete }}">{% trans 'Delete' %}</a>"""),
            )
        )


class LineForm(forms.ModelForm):

    class Meta:
        model = Line
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(LineForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Field('invoice', wrapper_class="col-md-12"),
            Field('reference', wrapper_class="col-md-4"),
            Field('concept', wrapper_class="col-md-4"),
            Field('quantity', wrapper_class="col-md-4"),
            Field('unit', wrapper_class="col-md-4"),
            Field('unit_price', wrapper_class="col-md-4"),
            Field('amount', wrapper_class="col-md-4"),
        )

        self.helper.layout.append(
            FormActions(
                Submit('submit', _('Submit'), css_class='btn btn-primary'),
                HTML("""{% load i18n %}<a class="btn btn-danger"
                        href="{{ url_delete }}">{% trans 'Delete' %}</a>"""),
            )
        )


class AddressesForm(forms.ModelForm):

    class Meta:
        model = Addresses
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AddressesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Field('autor', wrapper_class="col-md-4"),
            Field('address', wrapper_class="col-md-4"),
            Field('city', wrapper_class="col-md-4"),
        )

        self.helper.layout.append(
            FormActions(
                Submit('submit', _('Submit'), css_class='btn btn-primary'),
                HTML("""{% load i18n %}<a class="btn btn-danger"
                        href="{{ url_delete }}">{% trans 'Delete' %}</a>"""),
            )
        )
