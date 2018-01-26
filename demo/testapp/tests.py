# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import reverse
from django.contrib.auth.models import User, Permission, Group
from django.test.client import RequestFactory
from django.utils import timezone
from datetime import datetime, timedelta, tzinfo
#TEST
from django.test import ( TestCase,
                            Client )

#CRUD
from cruds_adminlte.utils import get_fields
from testapp.views import AutorCRUD, InvoiceCRUD, IndexView, CustomerCRUD, LineCRUD, AddressCRUD

from testapp import views as testapp_views
from cruds_adminlte import crud as crud_views

#APPs
from testapp.models import ( Autor, 
                             Addresses, 
                             Customer, 
                             Invoice, 
                             Line )
from django.conf import settings


class TreeData(TestCase):
    def setUp(self):
        self.app_testing='testapp'
        #self.model='invoice'
        #self.view = None
        nobjects=4 # number of objects to insert
        self.actions=['create', 'list', 'delete', 'update', 'detail']  
        
        self.factory = RequestFactory()
        #user to test
        self.user = User( username='test', email='test@example.com', is_active=True,
              is_staff=True, is_superuser=True,
        )
        self.user.set_password('test')
        self.user.save()
        
        
        # add objects Autor/Addressself.client.login(username='test', password='test')
        for i in range(nobjects):  # add Autor-Address 
             # autor 0   | autor 1   | autor 2   | autor 3
             # address 0 | address 1 | address 2 | address 3
            
             ao = Autor.objects.create(name="author_name_%i"%i)
             ado = Addresses(autor=ao)
             ado.name="addresses_address_%s_%i"%(ao.pk,i)
             ado.city="addresses_city_%s_%i"%(ao.pk,i)
             ado.save()
              
          
          
        # add object Customer/Invoices
        for i in range(nobjects):  # add Customer (Invoices < Lines)
            co = Customer.objects.create(name="customer_%i"%i,
                                          information="information_customer_%i"%i,
                                          email="customer_%i@examples.dj"%i,
                                         date = datetime.now(),
                                         time=datetime.now(),
                                         datetime=timezone.now()
                                         )
            
            
            # customer 0 | customer 1 | customer 2 | customer 3
            # -----------| ---------- | ---------- | ----------
            # invoice 0  | invoice 4  | invoice 8  | invoice 12
            # invoice 1  | invoice 5  | invoice 9  | invoice 13
            # invoice 2  | invoice 6  | invoice 10 | invoice 14
            # invoice 3  | invoice 7  | invoice 11 | invoice 15
                                                   
            io = Invoice.objects.create(customer=co,registered=True,sent=False,paid=False,date=timezone.now())  # only registered   
            io = Invoice.objects.create(customer=co,registered=True,sent=True,paid=False,date=timezone.now(),pk=None) # registered and sent
            io = Invoice.objects.create(customer=co,registered=False,sent=False,paid=False,date=timezone.now(),pk=None) # nothing did!
            io = Invoice.objects.create(customer=co,registered=True,sent=True,paid=True,date=timezone.now(),pk=None)  # completed

                      
        # add object Invoices / Lines
        for io in Invoice.objects.all():
             for i in range(nobjects):  
                 lo=Line(invoice=io)
                 lo.reference=io.customer.name+"_"+str(io.pk)+"_reference"+str(i)  #  customer_0 + 0 + _reference + 0
                 lo.concept=io.customer.name+"_"+str(io.pk)+"_concept"+str(i)   #  customer_0 + 0 + _concept + 0
                 lo.quantity="quantity_"+str(i)      #  quantity_0
                 lo.unit=i
                 lo.unit_price=i
                 lo.amount=i
                 lo.save()
            
                 # ( customer 0) -------------------------------------------------------------------------------------------
                 # invoice 0                                           | invoice 1
                 #   * Line 0 i=0                                      |  *   Line 4    i=0
                 #Line.reference=customer_0_0_reference_0              | Line.reference=customer_0_1_reference_0 
                 #Line.concept=customer_0_0_concept_0                  | Line.concept=customer_0_1_concept_0
                 #Line.concept=quantity_0                              | Line.concept=quantity_0           
                 #   * Line 1 i=1                                      |   *  Line 5    i=1
                 #Line.reference=customer_0_0_reference_1              | Line.reference=customer_0_5_reference_1           
                 #Line.concept=customer_0_0_concept_1                  | Line.reference=customer_0_5_concept_1                   
                 #Line.concept=quantity_1                              | Line.concept=quantity_1  
                 #   * Line 2 i=2  ...                                 |   *  Line 6   i=2   ...
                 #   * Line 3 i=3  ...                                 |   *  Line 7   i=3   ...              
                 #----------                      ----------------------------------                      -----------------   
                 # invoice 2                                           | invoice 3
                 #   * Line 8   i=0                                    |  *   Line 12   i=0
                 #Line.reference=customer_0_0_reference_0              | Line.reference=customer_0_1_reference_0 
                 #Line.concept=customer_0_0_concept_0                  | Line.concept=customer_0_1_concept_0
                 #Line.concept=quantity_0                              | Line.concept=quantity_0              
                 #   *  Line 9  i=1                                    |   *  Line 13   i=1
                 #Line.reference=customer_0_0_reference_1              | Line.reference=customer_0_1_reference_1           
                 #Line.concept=customer_0_0_concept_1                  | Line.reference=customer_0_1_concept_1                   
                 #Line.concept=quantity_1                              | Line.concept=quantity_1  
                 #   * Line 10 i=2  ...                                |   *  Line 14  i=2   ...
                 #   * Line 11 i=3  ...                                |   *  Line 15  i=3   ...                 
                 # ( customer 1) -------------------------------------------------------------------------------------------        


    def get_action_url(self,action,pk=None):
         if ( action in ['update','delete','detail'] ) :
                url= reverse(self.app_testing+'_'+self.model+'_'+action, kwargs={'pk': pk})    # testapp_invoice/1/update
         else:
                url= reverse(self.app_testing+'_'+self.model+'_'+action)    # testapp/invoice/create
                    
         return url                
        
class SimpleOListViewTest:
    
        """ Test show list of 'object_list' """
        def test_get_listView_content(self):
            self.client.login(username='test', password='test')
            url= reverse(self.app_testing+'_'+self.model+'_list')         

            response = self.client.get(url)
            self.assertEqual(response.status_code, 200 )
            
            if self.view.paginate_by :
                object_list=response.context['object_list']
                if (( len(object_list) == self.model_inserting) and (self.model_inserting < self.view.paginate_by)):
                    self.assertEqual(len(object_list), self.model_inserting)  # Number of objects
                else:
                   self.assertEqual(len(object_list), self.view.paginate_by)  # Number of object by pages

            
            self.assertEqual(self.view.views_available, response.context['views_available'])
            
            self.client.logout()   
        
        """ Test show only button of valid actions """         
        def test_get_listView_actions(self):
            self.client.login(username='test', password='test')
            url= reverse(self.app_testing+'_'+self.model+'_list')         
            
            
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200 )
            
            for action in self.actions:  # django actions ['create', 'list', 'delete', 'update', 'detail']
                 if action in self.view.views_available:  # crudview set actions ['create', 'list']
                    url=self.get_action_url(action,1)
                    self.assertContains( response, '<a href="'+url )          
                     

            self.client.logout()  
            
            
        """ Test show objecto by pagination 1 object and url pages bottons """         
        def test_get_listView_pagination(self):
            self.client.login(username='test', password='test')
            url= reverse(self.app_testing+'_'+self.model+'_list')         

            
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200 )
            
            if self.view.paginate_by :
                paginations=response.context['page_obj']
                if (self.model_inserting<=self.view.paginate_by):
                    self.assertTrue( ("<Page 1 of 1>") in ("%s"%paginations) ) # check pagina 1
                    self.assertFalse( ('Page %i '%self.view.paginate_by) in ("%s"%paginations) )
                else:
                    self.assertTrue( ("<Page 1 of %i>"%int(self.model_inserting/self.view.paginate_by)) in ("%s"%paginations) ) # check pagina 1
                
                # exist all buttons of paginations
                for i in range(1, int(self.model_inserting/self.view.paginate_by)):  # 16 = (4 custormers x 4 invoices)
                     self.assertContains( response, 'page=%i"> %i </a>'%(i,i) )  
                                
                     

            self.client.logout()    
            
class SimpleOListViewInvoiceTest(TreeData,SimpleOListViewTest):   
        def __init__(self, *args, **kwargs):
                self.model='invoice' 
                self.model_inserting=(4*4)       
                self.view = InvoiceCRUD()   # defined view
                super(SimpleOListViewInvoiceTest, self).__init__(*args, **kwargs)


class SimpleOListViewCustomerTest(TreeData,SimpleOListViewTest):   
        def __init__(self, *args, **kwargs):
                self.model='customer'        
                self.model_inserting=4*4
                self.view = CustomerCRUD()   # defined view 
                super(SimpleOListViewCustomerTest, self).__init__(*args, **kwargs)                
                      

                
                         
# """ Filters test """
# class FilterViewTest(InsertData):
#     def setUp(self):   
#         self.user = User(
#             username='test', email='test@example.com', is_active=True,
#             is_staff=True, is_superuser=True,
#         )
#         self.user.set_password('test')
#         self.user.save()
#         
#         #insertar Customer
#         #insert Invoice
#         #insert Line
#         
#  """ Models query test """
# class TestUtils(TestCase):
# 
#     def test_get_fields_order(self):
#         res = get_fields(Autor, ('name',))
#         self.assertEqual(list(res.keys())[0], 'name')
# 
#        
#         customer_0 + 0 + _concept
#     def test_listview(self):
#         self.client.login(username='test', password='test')
#         url=reverse('testapp_invoice_list')
#         url+="?customer=&invoice_number=&initial-invoice_number=&date=&line=16&line=17"
#         response = self.client.get(url)
#         print (response.context['object_list'])    
#         self.assertQuerysetEqual(response.context['object_list'], [])
#           
# 
# 
# 
# """ Views test """
# class AuthUserViewTest(TestCase):
# 
#     def setUp(self):
#         group_name = "My Test Group"
#         self.group = Group(name=group_name)
#         self.group.save()
#         
#         self.user = User(
#             username='test', email='test@example.com', is_active=True,
#             is_staff=True, is_superuser=True,
#         )
#         self.user.set_password('test')
#         self.user.save()
# 
#         
#     def test_user_noLogin(self):
#         """ The User don't have been login """
#         response = self.client.get(reverse('auth_user_list'))
#         #self.assertContains(response.context,url)
#         self.assertEqual(response.status_code, 302 )
#         self.assertEqual(response.url,"/accounts/login/?next=/lte/auth/user/list")
#         
#         
#         
#     def test_user_list(self):
#         """ The user can load the users list,  when it's login """
#         self.client.login(username='test', password='test')
#         response = self.client.get(reverse('auth_user_list'))
#         #print (response)
#         self.assertEqual(response.status_code, 200 )
#         self.assertQuerysetEqual(response.context['object_list'],['<User: test>'])
#         
#         
#     def test_user_group_list(self): 
#         """ The user can lad group, when it's login """
#         self.client.login(username='test', password='test')
#         response = self.client.get(reverse('auth_user_groups_list'))
#         #print (response)
#         self.assertQuerysetEqual(response.context['object_list'], [])
#                
#    
# """ Admin user views test"""
# class AdminViewTestCase(TestCase):
#     def setUp(self):
#         group_name = "My Test Group"
#         self.group = Group(name=group_name)
#         self.group.save()
#         
#         self.user = User(
#             username='test', email='test@example.com', is_active=True,
#             is_staff=True, is_superuser=True,
#         )
#         self.user.set_password('test')
#         self.user.save()
#         self.client.login(username='test', password='test')
#         
#         
#     def tearDown(self):
#         self.client.logout()
#                     
#     def test_user_can_access(self):
#         """user in group should have access
#         """
#         self.user.groups.add(self.group)
#         self.user.save()
#         self.client.login(username='test', password='test')
#         response = self.client.get(reverse('auth_user_list'))
#         self.assertEqual(response.status_code, 200)      
#         
#             
#     def test_admin_not_broken(self):
#         """ user can use django admin """
#         response = self.client.get('/admin/')
#         self.assertContains(response, '/admin/password_change/')
#         self.assertNotContains(response, "You don't have permission to edit anything")
# 
#     def test_admin_auth_not_broken(self):
#         """ user can init auth """
#         response = self.client.get('/admin/auth/')
#         self.assertEqual(response.status_code, 200, response)