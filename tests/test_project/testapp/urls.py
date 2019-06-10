# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from testapp.views import AuthorCRUD

urlpatterns = [
    ] + AuthorCRUD().get_urls()
