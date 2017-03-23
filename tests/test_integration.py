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
        response = self.client.get('/testapp/author/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Foo')

    def test_create(self):
        response = self.client.get('/testapp/author/new/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/testapp/author/new/', {
            'name': 'Bar',
        })
        instance = Author.objects.filter(name='Bar').get()
        self.assertRedirects(response, '/testapp/author/%s/' % instance.pk)

    def test_detail(self):
        response = self.client.get('/testapp/author/%s/' %
                                   self.author.pk)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Foo')

    def test_update(self):
        url = '/testapp/author/%s/edit/' % self.author.pk
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url, {
            'name': 'Fooz',
        })
        self.assertRedirects(response, '/testapp/author/%s/' % self.author.pk)

    def test_delete(self):
        url = '/testapp/author/%s/remove/' % self.author.pk
        response = self.client.post(url)
        self.assertEqual(Author.objects.count(), 0)
        self.assertRedirects(response, '/testapp/author/')
