=============================
django-cruds
=============================

* Note: This version of django-cruds is based on bmihelac's one (https://github.com/bmihelac/django-cruds/)

django-cruds is simple drop-in django app that creates CRUD (Create, read,
update and delete) views for existing models and apps.

django-cruds goal is to make prototyping faster.


Documentation
-------------

To add CRUD for whole app, add this to urls.py::

    # django-cruds
    from cruds.urls import crud_for_app
    urlpatterns += crud_for_app('testapp')

This will create following urls and appropriate views (assuming
there is a application named ``testapp`` with model ``Author``:

===================================== =====================
URL                                   name
===================================== =====================
/testapp/author/                      testapp_author_list
/testapp/author/new/                  testapp_author_create
/testapp/author/(?P<pk>\d+)/          testapp_author_detail
/testapp/author/(?P<pk>\d+)/edit/     testapp_author_update
/testapp/author/(?P<pk>\d+)/remove/   testapp_author_delete
===================================== =====================

It is also possible to add CRUD for one model::

    from django.db.models.loading import get_model
    from cruds.urls import crud_for_model
    urlpatterns += crud_for_model(get_model('testapp', 'Author'))

``crud_fields`` templatetag displays fields for an object::

    {% load crud_tags %}

    <table class="table">
      <tbody>
        {% crud_fields object "name, description" %}
      </tbody>
    </table>

Use ``cruds.util.crud_url`` shortcut function to quickly get url for
instance for given action::

    crud_url(author, 'update')

Is same as::

        reverse('testapp_author_update', kwargs={'pk': author.pk})

If you want to override a form with some other crispy features you can add to
your testapp.urls the following:

    urlpatterns = []
    urlpatterns += [
        url(r'author/new/$',
            CRUDCreateView.as_view(model=Author, form_class=AuthorForm),
            name='testapp_author_update'),
        url(r'author/(?P<pk>\d+)/edit/$',
            CRUDUpdateView.as_view(model=Author, form_class=AuthorForm),
            name='testapp_customer_update'),
    ]

And define the AuthorForm with tabs or any other crispy feature in your app:

    self.helper.layout = Layout(
        TabHolder(
            Tab(
                _('Basic information'),
                Field('name', wrapper_class="col-md-6"),
                Field('address', wrapper_class="col-md-6"),
                Field('email', wrapper_class="col-md-12"),
            ),
            Tab(
                _('Other information'),
                Field('image', wrapper_class="col-md-6"),
                Field('cropping', wrapper_class="col-md-6"),
                Field('cif', wrapper_class="col-md-6"),
                Field('slug', wrapper_class="col-md-6")
            )
        )
    )

You will get something similar to this:

.. image:: doc/cruds-form.png


Templates
^^^^^^^^^

django-cruds views will append CRUD template name to a list of default
candidate template names for given action.

CRUD Templates are::

    cruds/create.html
    cruds/delete.html
    cruds/detail.html
    cruds/list.html
    cruds/update.html

Templates are based in AdminLTE2 (https://almsaeedstudio.com/themes/AdminLTE/index2.html)
and django-adminlte2 (https://github.com/adamcharnock/django-adminlte2). They're
ready to run with:

* django-crispy-forms (https://django-crispy-forms.readthedocs.io/en/latest/)
* select2 (https://select2.github.io/)
* django-cropping-image (https://github.com/jonasundderwolf/django-image-cropping)

If you want to override the sidebar you can do it creating a file called
``templates/adminlte/lib/_main_sidebar.html`` inside your project and you can
put there the contents you want.

Quickstart
----------

Install django-cruds::

    pip install django-cruds

Then use it in a project, add ``cruds`` to ``INSTALLED_APPS``. Note that you
will have to install ``crispy_forms`` and ``image_cropping`` if before the app
if you want to use them:

    pip install django-crispy-forms
    pip install easy-thumbnails
    pip install django-image-cropping


Requirements
------------

* Python 2.7+
* Django >=1.4.2
* django-crispy-forms
