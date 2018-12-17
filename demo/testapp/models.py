# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from image_cropping import ImageCropField, ImageRatioField
from testapp.presentation import InvoicePresentation


# Create your models here.
class Autor(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('pk',)
        permissions = (
            ("view_author", "Can see available Authors"),
        )


class Addresses(models.Model):
    autor = models.ForeignKey(Autor, related_name="Autor",
                              on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    status = models.BooleanField(_("Status"), help_text=_('Active?'),
                                 default=True)

    class Meta:
        ordering = ('pk',)
        permissions = (
            ("view_addresses", "Can see available Addresses"),
        )


class Customer(models.Model):
    name = models.CharField(_('Customer'), max_length=200)
    information = models.TextField()
    email = models.EmailField()

    image = ImageCropField(upload_to='media/customers', blank=True,)
    cropping = ImageRatioField('image', '430x360')
    color = models.CharField(max_length=10)

    date = models.DateField()
    time = models.TimeField()
    datetime = models.DateTimeField()

    class Meta:
        ordering = ('pk',)
        permissions = (
            ("view_customer", "Can see available customers"),
        )


def last_number():
    try:
        inv = Invoice.objects.all().order_by('-date')[0].invoice_number
        return int(inv) + 1
    except:
        return 1


class Invoice(models.Model, InvoicePresentation):

    customer = models.ForeignKey(Customer, related_name="customer",
                                 on_delete=models.CASCADE)
    registered = models.BooleanField(_("Registered"),
                                     help_text=_('Registered yet?'))
    sent = models.BooleanField(_("Sent"), help_text=_('Invoice sent?'))
    paid = models.BooleanField(_("Paid"),
                               help_text=_('Invoice paid?'))
    date = models.DateTimeField(_('Creation date'))
    invoice_number = models.CharField(_('Invoice Number'),
                                      default=last_number,
                                      max_length=50)
    description1 = models.TextField(_('Description header'), blank=True)
    description2 = models.TextField(_('Description footer'), blank=True)
    subtotal = models.CharField(_('Subtotal'), blank=True,
                                max_length=200,
                                help_text=_('Calculated field'))
    subtotal_iva = models.CharField(_('Subtotal IVA'), blank=True,
                                    max_length=200,
                                    help_text=_('Calculated field'))
    subtotal_retentions = models.CharField(_('Subtotal Retentions'),
                                           blank=True, max_length=200,
                                           help_text=_('Calculated field'))
    total = models.CharField(_('Total'), max_length=200, blank=True,
                             help_text=_('Calculated field'))

    def __unicode__(self):
        return str(self.invoice_number) + "->" + str(self.date)

    class Meta:
        ordering = ('pk',)
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
        permissions = (
            ("view_invoice", "Can see available Invoices"),
        )


class Line(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="line",
                                on_delete=models.CASCADE)
    reference = models.CharField(_('Reference'), max_length=200)
    concept = models.CharField(_('Concept'), max_length=200)
    quantity = models.CharField(_('Quantity'), max_length=200)
    unit = models.CharField(_('Unit'), help_text=_('(days, hours...)'),
                            max_length=200)
    unit_price = models.CharField(_('Unit Price'), max_length=200)
    amount = models.CharField(_('Ammount'), max_length=200)

    def __unicode__(self):
        return self.reference + " " + self.quantity + "x" + self.unit_price

    class Meta:
        ordering = ('pk',)
        verbose_name = _('Line')
        verbose_name_plural = _('Lines')
        permissions = (
            ("view_line", "Can see available lines"),
        )
