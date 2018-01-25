# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from django.contrib.auth.models import User, Permission, Group

#TEST
from django.test import TestCase
from django.test import Client

#CRUD
from cruds_adminlte.utils import get_fields
from cruds_adminlte import crud as crud_views

#APPs
from .models import Autor, Customer, Line,  

class InsertData(TestCase):



""" Filters test """
class FilterViewTest(InsertData):
    def setUp(self):   
        self.user = User(
            username='test', email='test@example.com', is_active=True,
            is_staff=True, is_superuser=True,
        )
        self.user.set_password('test')
        self.user.save()
        
        #insertar Customer
        #insert Invoice
        #insert Line
        
        
        
    def test_listview(self):
        self.client.login(username='test', password='test')
        url=reverse('testapp_invoice_list')
        url+="?customer=&invoice_number=&initial-invoice_number=&date=&line=16&line=17"
        response = self.client.get(url)
        print (response.context['object_list'])    
        self.assertQuerysetEqual(response.context['object_list'], [])
          



""" Views test """
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
               
   
""" Admin user views test"""
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
        """ user can use django admin """
        response = self.client.get('/admin/')
        self.assertContains(response, '/admin/password_change/')
        self.assertNotContains(response, "You don't have permission to edit anything")

    def test_admin_auth_not_broken(self):
        """ user can init auth """
        response = self.client.get('/admin/auth/')
        self.assertEqual(response.status_code, 200, response)
       