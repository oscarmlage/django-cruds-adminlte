# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, RequestFactory
from django.urls import reverse


class CRUDMixinTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_add_crud_template(self):
        request = self.factory.get('')
        url = reverse('testapp_author_list')
        self.assertEqual(url, "/testapp/author/list")

        # TODO: simulate the request and check templates used.
        # self.assertEqual(view.template_name, [
        #    u'testapp/author_list.html',
        #    u'cruds/list.html',
        # ])
