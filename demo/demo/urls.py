"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from cruds_adminlte.urls import crud_for_app
from testapp.views import (AutorCRUD, InvoiceCRUD, IndexView, CustomerCRUD,
                           LineCRUD, AddressCRUD)
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

authorcrud = AutorCRUD()
invoicecrud = InvoiceCRUD()
customercrud = CustomerCRUD()
linecrud = LineCRUD()
addresscrud = AddressCRUD()


urlpatterns = [
    url(r'^$', IndexView.as_view()),

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
