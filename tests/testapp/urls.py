# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include

from cruds_adminlte.urls import crud_for_app

urlpatterns = [
    url(r'^select2/', include('django_select2.urls')),
]

urlpatterns += crud_for_app('testapp', login_required=True, check_perms=True)
