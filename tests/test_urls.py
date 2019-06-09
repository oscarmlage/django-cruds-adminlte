""" Test the helpers in cruds_adminlte.urls
"""
from cruds_adminlte.urls import crud_for_app


def test_crud_for_model():
    # TODO: Write proper tests
    pass


def test_crud_for_app(settings, client):
    # TODO :write proper tests
    crud = crud_for_app('testapp')
    pass
