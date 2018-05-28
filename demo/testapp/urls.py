from cruds_adminlte.urls import crud_for_app

app_name = 'testapp'

urlpatterns = []

urlpatterns += crud_for_app(app_name, check_perms=True, namespace="ns")
