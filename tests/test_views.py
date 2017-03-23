# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, RequestFactory

from cruds import views as crud_views

from tests.testapp.models import (
    Author,
)


class CRUDMixinTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_add_crud_templat(self):
        request = self.factory.get('')
        view = crud_views.CRUDListView.as_view(model=Author)(request)
        self.assertEqual(view.template_name, [
            u'testapp/author_list.html',
            u'cruds/list.html',
        ])
