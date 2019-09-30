from django.conf import settings
from django.conf.urls import url, include
from django.urls import path

from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render

from cruds_adminlte.urls import crud_for_app
from testapp.views import (AutorCRUD, InvoiceCRUD, IndexView, CustomerCRUD,
                           LineCRUD, AddressCRUD)
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static


def hello_page(request):
    """Simple view to say hello.

    It is used to check the authentication system.
    """
    text = "Welcome to test_project"
    if not request.user.is_anonymous:
        text = "Welcome '%s' to test_project" % request.user.username
    return HttpResponse(text, content_type='text/plain')


authorcrud = AutorCRUD()
invoicecrud = InvoiceCRUD()
customercrud = CustomerCRUD()
linecrud = LineCRUD()
addresscrud = AddressCRUD()


urlpatterns = [
    url(r'^$', IndexView.as_view()),
    path('hello', hello_page, name='hello_page'),
    path('', lambda r: render(r, template_name="homepage.html"), name="home"),
    path('ta/', include('testapp.urls')),

    url(r'^accounts/login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^select2/', include('django_select2.urls')),
    url('^namespace/', include('testapp.urls')),
    url(r'', include(authorcrud.get_urls())),
    url(r'', include(invoicecrud.get_urls())),
    url(r'', include(customercrud.get_urls())),
    url(r'', include(linecrud.get_urls())),
    url(r'', include(addresscrud.get_urls())),
]


urlpatterns += crud_for_app('auth', login_required=True, cruds_url='lte')


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
