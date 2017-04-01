# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template


register = template.Library()


@register.filter
def get(dic, key):
    """
    Filter returns dict's associated value.
    """
    return dic[key]
