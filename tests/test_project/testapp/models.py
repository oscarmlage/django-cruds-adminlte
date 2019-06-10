# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Author(models.Model):
    name = models.CharField(max_length=100)
    birthday = models.DateField()

    class Meta:
        ordering = ['-name', ]

    def __str__(self):
        return self.name
