# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test.testcases import TestCase

from cruds_adminlte.utils import get_fields

from tests.testapp.models import (
    Author,
)


class TestUtils(TestCase):

    def test_get_fields_order(self):
        res = get_fields(Author, ('birthday', 'name'))
        self.assertEqual(list(res.keys())[0], 'birthday')
