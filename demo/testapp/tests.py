# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from django.contrib.auth.models import User, Permission, Group

#TEST
from django.test import TestCase, RequestFactory
from django.test import Client

#CRUD
from cruds_adminlte.utils import get_fields
from cruds_adminlte import crud as crud_views

#APPs
from .models import Autor


class CRUDViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_add_crud_template(self):
        request = self.factory.get('')
        view = crud_views.CRUDView.as_view(model=Author)(request)
        self.assertEqual(view.template_name, [
            u'testapp/author_list.html',
            u'cruds/list.html',
        ])


class TestUtils(TestCase):

    def test_get_fields_order(self):
        res = get_fields(Autor, ('name',))
        self.assertEqual(list(res.keys())[0], 'name')




""" TEST OF VIEWS """
class AuthUserViewTest(TestCase):

    def setUp(self):
        group_name = "My Test Group"
        self.group = Group(name=group_name)
        self.group.save()
        
        self.user = User(
            username='test', email='test@example.com', is_active=True,
            is_staff=True, is_superuser=True,
        )
        self.user.set_password('test')
        self.user.save()
      

        
        
    def test_user_noLogin(self):
        """ The User don't have been login """
        response = self.client.get(reverse('auth_user_list'))
        #self.assertContains(response.context,url)
        self.assertEqual(response.status_code, 302 )
        self.assertEqual(response.url,"/accounts/login/?next=/lte/auth/user/list")
        
        
        
    def test_user_list(self):
        """ The user can load the users list,  when it's login """
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('auth_user_list'))
        #print (response)
        self.assertEqual(response.status_code, 200 )
        self.assertQuerysetEqual(response.context['object_list'],['<User: test>'])
        
        
    def test_user_group_list(self): 
        """ The user can lad group, when it's login """
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('auth_user_groups_list'))
        #print (response)
        self.assertQuerysetEqual(response.context['object_list'], [])
               
   
class AdminViewTestCase(TestCase):
    def setUp(self):
        group_name = "My Test Group"
        self.group = Group(name=group_name)
        self.group.save()
        
        self.user = User(
            username='test', email='test@example.com', is_active=True,
            is_staff=True, is_superuser=True,
        )
        self.user.set_password('test')
        self.user.save()
        self.client.login(username='test', password='test')
        
        
    def tearDown(self):
        self.client.logout()
                    
    def test_user_can_access(self):
        """user in group should have access
        """
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('auth_user_list'))
        self.assertEqual(response.status_code, 200)      
        
            
    def test_admin_not_broken(self):
        response = self.client.get('/admin/')
        self.assertContains(response, '/admin/password_change/')
        self.assertNotContains(response, "You don't have permission to edit anything")

    def test_admin_auth_not_broken(self):
        response = self.client.get('/admin/auth/')
        self.assertEqual(response.status_code, 200, response)
       