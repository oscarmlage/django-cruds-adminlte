# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test.testcases import TestCase

from tests.testapp.models import (
    Author,
)


class TestIntegration(TestCase):

    def setUp(self):
        self.author = Author.objects.create(name='Foo')

    def test_list(self):
        self.assertEqual(1, 1)
