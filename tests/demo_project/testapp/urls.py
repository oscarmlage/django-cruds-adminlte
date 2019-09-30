from cruds_adminlte.urls import crud_for_app
from .views import AuthorCRUD
app_name = 'testapp'

urlpatterns = [
    ] + AuthorCRUD().get_urls()

urlpatterns += crud_for_app(app_name, check_perms=True, namespace="ns")
