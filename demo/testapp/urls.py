from . import views
from cruds_adminlte.urls import crud_for_app
from django.conf.urls import url, include



app_name = 'testapp'

urlpatterns=[ ]
    

urlpatterns+= crud_for_app('testapp', check_perms=True)

