# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cruds_adminlte.utils import get_fields, ACTION_CREATE, ACTION_DETAIL, ACTION_UPDATE, ACTION_DELETE, ACTION_LIST, \
    crud_url_name
from testapp.models import (
    Author,
)


def test_get_fields_ordering():
    """ get_fields should return fields in appropiate order. """
    res = get_fields(Author, ('birthday', 'name'))
    assert [r for r in res] == ['birthday', 'name']


def test_crud_url_name():
    model = Author
    app_label = model._meta.app_label
    model_lower = model.__name__.lower()

    actions = [ACTION_CREATE, ACTION_DELETE,
               ACTION_DETAIL, ACTION_LIST,
               ACTION_UPDATE]
    for a in actions:
        urlname = crud_url_name(model, a)
        assert urlname == "%s_%s_%s" % (app_label, model_lower, a)
        urlname = crud_url_name(model, a, 'prefix')
        assert urlname == "prefix%s_%s_%s" % (app_label, model_lower, a)
