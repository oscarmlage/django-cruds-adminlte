===============
CRUDView Usage
===============


Using CRUDView
----------------

CRUDView is a generic way to provide create, list, detail, update, delete views
in one class, you can inherit for it and manage login_required, model perms,
pagination, update and add forms

How to use:

In your views file create a class inherit for CRUDView

.. code:: python

    from testapp.models import Customer
    from cruds_adminlte.crud import CRUDView
    class Myclass(CRUDView):
        model = Customer

In urls.py

.. code:: python

    myview = Myclass()
    urlpatterns = [
        url('path', include(myview.get_urls()))  # also support
                                                 # namespace
    ]

If you want to filter views add views_available list

.. code:: python

    class Myclass(CRUDView):
        model = Customer
        views_available=['create', 'list', 'delete', 'update', 'detail']

Permissions
------------

The default behavior is check_login = True and check_perms=True but you can
turn off with

.. code:: python

    from testapp.models import Customer
    from cruds_adminlte.crud import CRUDView

    class Myclass(CRUDView):
        model = Customer
        check_login = False
        check_perms = False

You also can defined extra perms with

.. code:: python

    class Myclass(CRUDView):
        model = Customer
        perms = { 'create': ['applabel.mycustom_perm'],
                  'list': [],
                  'delete': [],
                  'update': [],
                  'detail': []
                }

If check_perms = True we will add default django model perms
(<applabel>.[add|change|delete|view]_<model>) ej. mytestapp.add_mymodel

.. warning::
    applabel.view_model are not part of django perms, so needs to be create
    in models metadata ej.

    .. code:: python

        class Autor(models.Model):
            name = models.CharField(max_length=200)
            class Meta:
                ordering = ('pk',)
                permissions = (
                    ("view_author", "Can see available Authors"),
                    )

    applabel.view_model is used by default for list perm, so if it's not
    created then list view raise 503 permission denied (with screen in browser)


Searching
------------

As django admin does, **search_fields** are available, and you can filter using
double underscore (__) to search across the objects.

**split_space_search** split search text in parts using the string provided,
this can be usefull to have better results but have impact in search
performance, if split_space_search is True then ' ' is used

.. code:: python

    class Myclass(CRUDView):
        model = Customer
        search_fields = ['description__icontains']
        split_space_search = ' ' # default False

.. note:: 'icontains' is not set by default as django admin does, so you need
          to set if not equal search is wanted

.. image:: https://raw.githubusercontent.com/oscarmlage/django-cruds-adminlte/master/docs/images/cruds-search.png
    :target: https://raw.githubusercontent.com/oscarmlage/django-cruds-adminlte/master/docs/images/cruds-search.png


Overwrite forms
-------------------

You can also overwrite add and update forms

.. code:: python

    class Myclass(CRUDView):
        model = Customer
        add_form = MyFormClass
        update_form = MyFormClass


Overwrite templates
----------------------

And of course overwrite base template name

.. code:: python

    class Myclass(CRUDView):
        model = Customer
        template_name_base = "mybase"

Remember basename is generated like app_label/modelname if template_name_base
is set as None add 'cruds' by default so template loader search this structure

.. code:: bash

    basename + '/create.html'
    basename + '/detail.html'
    basename + '/update.html'
    basename + '/list.html'
    basename + '/delete.html'

.. Note::
    Also import <applabel>/<model>/<basename>/<view type>.html


Using namespace
-----------------

There is no way to create 2 CRUDView to the same model, because urls could be
crash, so namespace come to help with this, `namespace` are part of django urls
system and allows to have same urls with diferent context, so you can use this
to add different behaivior to a model, also different urls.

In views

.. code:: python

    from testapp.models import Customer
    from cruds_adminlte.crud import CRUDView
    class Myclass(CRUDView):
        model = Customer
        namespace = "mynamespace"

In urls.py

.. code:: python

    myview = Myclass()
    urlpatterns = [
        url('path', include(myview.get_urls(),
                            namespace="mynamespace"))
    ]

Namespace in views and urls needs to match, or url match problem are raise.

Decorators
-------------------

CRUDViews use a generic Django views and provide some utilities to manage
decorator. As django documentation say you can use decorator in urls when you
call as_view method in generic views like.

In urls.py

.. code:: python

    urlpatterns = [
        url('list', login_required(ListView.as_view()) )
    ]

CRUDViews take advantage of this and create this methods

- decorator_create(self, viewclass)
- decorator_detail(self, viewclass)
- decorator_list(self, viewclass)
- decorator_update(self, viewclass)
- decorator_delete(self, viewclass)

So you can overwrite it and put your own decorator.  Be warried about
login_required decorator, because when check_login is set we used this method
to insert login_required decorator.

How to overwrite:

In views

.. code:: python

    from testapp.models import Customer
    from cruds_adminlte.crud import CRUDView
    class Myclass(CRUDView):
        model = Customer
        def decorator_list(self, viewclass):
            viewclass = super(Myclass, self).decorator_list(viewclass) # help with
                                                                       # login_required
            return mydecorator(viewclass)


Overwrite views
-------------------

Overwrite views are easy because we are using django generic views, but you
need to have some worry.

If you don't need to overwrite this functions

- get_template_names
- get_context_data
- dispatch
- paginate_by attr in list view

then you can overwrite and return your own class

- get_create_view_class
- get_update_view_class
- get_detail_view_class
- get_list_view_class
- get_delete_view_class

but if you need to overwrite some of the above functions you need to overwrite

- get_create_view
- get_update_view
- get_detail_view
- get_list_view
- get_delete_view

Like

.. code:: python

    from testapp.models import Customer
    from cruds_adminlte.crud import CRUDView
    class Myclass(CRUDView):
        model = Customer
        def get_list_view(self):
            ListViewClass = super(Myclass, self).get_list_view()
            class MyListView(ListViewClass):
                def get_context_data(self):
                    context = super(MyListView, self).get_context_data()
                    return context
            return MyListView

.. warning::
    It's really important that you use *super(MyListView,
    self).get_context_data()* instead of ListView.get_context_data() because we
    insert some extra context there.

===================
UserCRUDView Usage
===================

A usefull utility class is provided named as UserCRUDView, and works link
CRUDView but include user management, but require than base model has user
attribute.

In Create and Update view save the model adding current user as user attribute.
In List View filter objects using current user.

In models

.. code:: python

    from django.contrib.auth.models import User
    from django.db import models
    class Customer(models.Model):
        user = models.ForeignKey(User)
        ...

In views

.. code:: python

    from testapp.models import Customer
    from cruds_adminlte.crud import CRUDView
    class Myclass(UserCRUDView):
        model = Customer

======================
InlineAjaxCRUD Usage
======================

Inlines works like django admin inlines but with some diferences, firts use
django-ajax for provide a crud view, and second not inlines in create view
(sorry for now we need model created to have pk reference).

Basically works like CRUDView and support all cases described above.  Require
this extra parameters

1. `base_model` model used to refence the inline
2. `inline_field` field used to update object, needs to be the same class
that `base_model`
3. `title` title of the inline (used to show separation betwen model fields
and inline fields).


.. code:: python

    class Address_AjaxCRUD(InlineAjaxCRUD):
        model = Addresses
        base_model = Autor
        inline_field = 'autor'
        fields = ['address', 'city']
        title = _("Addresses")

    class AutorCRUD(CRUDView):
        model = Autor
        inlines = [Address_AjaxCRUD]


