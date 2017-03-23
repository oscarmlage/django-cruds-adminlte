# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url, include
from django.contrib import admin

from cruds.urls import (
    crud_for_app,
)


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
)


# add crud for whole app
urlpatterns += crud_for_app('testapp')
