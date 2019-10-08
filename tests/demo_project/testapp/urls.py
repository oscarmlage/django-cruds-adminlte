from django.conf.urls import url, include
from testapp.views import (AuthorCRUD, InvoiceCRUD, IndexView, CustomerCRUD,
                           LineCRUD, AddressCRUD)

authorcrud = AuthorCRUD()
invoicecrud = InvoiceCRUD()
customercrud = CustomerCRUD()
linecrud = LineCRUD()
addresscrud = AddressCRUD()

urlpatterns = [
    url(r'^$', IndexView.as_view()),
    url(r'', include(authorcrud.get_urls())),
    url(r'', include(invoicecrud.get_urls())),
    url(r'', include(customercrud.get_urls())),
    url(r'', include(linecrud.get_urls())),
    url(r'', include(addresscrud.get_urls())),
    ]
