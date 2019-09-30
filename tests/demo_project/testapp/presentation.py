'''
Created on 29 abr. 2017

@author: luisza
'''
from django.utils.html import format_html


class InvoicePresentation:

    def get_description1_display(self):
        return format_html(self.description1)

    def get_description2_display(self):
        return format_html(self.description2)
