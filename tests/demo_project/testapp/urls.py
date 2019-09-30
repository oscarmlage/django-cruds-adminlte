from cruds_adminlte.urls import crud_for_app
from .views import AutorCRUD
app_name = 'testapp'

urlpatterns = [
    ] + AutorCRUD().get_urls()

urlpatterns += crud_for_app(app_name, check_perms=True, namespace="ns")
