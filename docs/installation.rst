============
Installation
============

.. _quickstart:

Quickstart
==========

Install django-cruds-adminlte (`already in Pypi <https://pypi.python.org/pypi/django-cruds-adminlte>`_)::

    pip install django-cruds-adminlte

Then use it in a project, add ``cruds_adminlte`` to ``INSTALLED_APPS``. Note
that you will have to install ``crispy_forms`` and ``image_cropping`` if
before the app if you want to use them: ::

    pip install django-crispy-forms
    pip install easy-thumbnails
    pip install django-image-cropping
    pip install djangoajax

Next step is to add the urls to your ``project.urls`` as was said above: ::

    # django-cruds-adminlte
    from cruds_adminlte.urls import crud_for_app
    urlpatterns += crud_for_app('testapp')

And you can start modeling your app, migrate it and directly browse to the urls
described above, that's all.


.. _requirements:

Requirements
============

.. highlight:: console

The django-cruds-adminlte works thanks to:

* Python 3.7+
* Django >=2.2
* django-crispy-forms
* django-image-cropping and easy-thumbnails (optional if you want to crop)
* djangoajax (for the inlines stuff)

If you want full support then install dependencies make sure to install these
packages prior to installation in your environment: ::

    pip install django-crispy-forms
    pip install django-select2
    pip install django-image-cropping
    pip install easy-thumbnails
    pip install djangoajax


.. _getting-the-code:

Getting the code
================

.. highlight:: console

For the latest stable version of django-cruds-adminlte use :program:`pip`: ::

  $ pip install django-cruds-adminlte

You could also retrieve the last sources from
https://github.com/oscarmlage/django-cruds-adminlte. Clone the repository
using :program:`git` and run the installation script: ::

  $ git clone git://github.com/oscarmlage/django-cruds-adminlte.git
  $ cd django-cruds-adminlte
  $ python setup.py install

or more easily via :program:`pip`: ::

  $ pip install -e git://github.com/oscarmlage/django-cruds-adminlte.git


.. _applications:

Applications
============

.. highlight:: python

Assuming that you have an already existing Django project, register
:mod:`cruds_adminlte` in the :mod:`INSTALLED_APPS` section of your
project's settings: ::

  INSTALLED_APPS = (
    ...
    'crispy_forms',
    'django_select2',
    'easy_thumbnails',
    'image_cropping',
    'django_ajax',
    'cruds_adminlte'
  )

.. _configuration:

Configuration
=============

.. highlight:: python

Configure template pack and jquery for :mod:`image_cropping`. Note: Template
also import jquery so it's not necessary import custom
:mod:`IMAGE_CROPPING_JQUERY_URL`: ::

    CRISPY_TEMPLATE_PACK = 'bootstrap3'
    IMAGE_CROPPING_JQUERY_URL = None

Configure internal IPs: ::

    INTERNAL_IPS = ('127.0.0.1',)

Configure :mod:`easy_thumbnails`: ::

    from easy_thumbnails.conf import Settings as thumbnail_settings
    THUMBNAIL_PROCESSORS = (
        'image_cropping.thumbnail_processors.crop_corners',
    ) + thumbnail_settings.THUMBNAIL_PROCESSORS

Configure the default time and datetime: ::

    TIME_FORMAT= 'h:i A'
    DATETIME_FORMAT='m/d/Y H:i:s'
    DATE_FORMAT="m/d/Y"

    TIME_INPUT_FORMATS = ['%I:%M %p']

.. warning::
    Datetime and time depends on `USE_TZ` attribute, so changes there impact in all django timezone management

.. _urls:

URLs for the CRUD
=================

To add CRUD for whole app, add this to :file:`urls.py`: ::

    # django-cruds-adminlte
    from cruds_adminlte.urls import crud_for_app
    urlpatterns += crud_for_app('testapp')

This will create following urls and appropriate views (assuming
there is a application named ``testapp`` with model ``Author``:

===================================== =====================
URL                                   name
===================================== =====================
/testapp/author/list/                 testapp_author_list
/testapp/author/new/                  testapp_author_create
/testapp/author/(?P<pk>\d+)           testapp_author_detail
/testapp/author/(?P<pk>\d+)/update/   testapp_author_update
/testapp/author/(?P<pk>\d+)/delete/   testapp_author_delete
===================================== =====================

It is also possible to add CRUD for one model: ::

    from django.apps import apps
    from cruds_adminlte.urls import crud_for_model
    urlpatterns += crud_for_model(apps.get_model('testapp', 'Author'))

cruds_for_app
=============

Parameters you can set in `cruds_for_app` method call:

* login_required (boolean): Check if the login is required, need to activate
  'login' and 'logout' urls, for example: ::

    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

* check_perms (boolean): Check if the user has the proper permissions.
* cruds_url (string): Put all the generated cruds in a common url, instead of
  'app_one/model/list' and 'app_two/model/list' we can set it to 'myadmin' and
  then the urls will be 'myadmin/app_one/model/list' and
  'myadmin/app_two/model/list'.
* modelconfig: Load custom model configs for the cruds of the model.

Different samples: ::

    urlpatterns += crud_for_app('app_one', login_required=True,
                                check_perms=True, cruds_url='myadmin')
    urlpatterns += crud_for_app('app_two', login_required=False,
                                check_perms=True, cruds_url='myadmin')

    from testapp.forms import CustomerForm, InvoiceForm
    model_config = {
    'add_customer': CustomerForm,	        'customer': {
    'update_customer': CustomerForm,	            'add_form': CustomerForm,
    'add_invoice': InvoiceForm,	            'update_form': CustomerForm,
    'update_invoice': InvoiceForm,	            'display_fields': ['name', 'information', 'email', 'image'],
        'search_fields': ['name__icontains', 'email__icontains'],
    },
    'invoice': {
        'add_form': InvoiceForm,
        'update_form': InvoiceForm,
    }
    urlpatterns += crud_for_app('app_three', login_required=True,
                                check_perms=True, cruds_url='myadmin',
                                modelconfig=model_config)
