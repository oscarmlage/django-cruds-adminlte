from cruds_adminlte.crud import CRUDView
from testapp.models import Author


class AuthorCRUD(CRUDView):
    model = Author
    search_fields = ('name__icontains', )
    views_available = ['create', 'list', 'update', 'detail', 'delete']
    check_perms = True
    check_login = True


