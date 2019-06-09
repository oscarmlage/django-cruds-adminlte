from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path, include


def hello_page(request):
    text = "Welcome to test_project"
    if not request.user.is_anonymous:
        text = "Welcome '%s' to test_project" % request.user.username
    return HttpResponse(text, content_type='text/plain')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello', hello_page, name='hello_page'),
    path('', lambda r: render(r, template_name="homepage.html"), name="home"),
    path('select2/', include('django_select2.urls')),
    path('ta/', include('testapp.urls')),
]
