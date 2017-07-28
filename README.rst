=====================
django-cruds-adminlte
=====================

``django-cruds-adminlte`` is simple drop-in django app that creates CRUD (Create, read,
update and delete) views for existing models and apps.

``django-cruds-adminlte goal`` is to make prototyping faster.

* Note: This version of ``django-cruds-adminlte`` is based on `bmihelac's one <https://github.com/bmihelac/django-cruds/>`_.


.. _historygoal:

History and goal
================

Developers spends a lot of time just doing cruds, ``Django built-in admin`` was
pretty and really nice... years ago. Right now customers (and people in
general) are more used to the web and they want to change whatever on their
smartphones, upload images cropping the important part, they're used to
``select2`` (or similar) in selects with so many options, etc..

A friend of mine told me to try backpack for laravel
(https://backpackforlaravel.com/), well in fact he showed me a demo. I was
impressed with what he could do just configuring a bit the models and the forms:

* Responsive design, more or less I guess you could use
  ``django-flat-responsive`` for that
* Tabbed forms: really easy to place fields in tabs, imho much more useful for
  the end user if the form is complex and has many fields (I've found nothing
  similar for django's admin)
* Wrappable fields: You can define the wrapper of the label+input (col-6,
  col-12), so it's easy to place fields side-by-side or 3 in a row, etc...
  You can do the same with ``django-crispy-forms`` but I've seen no easy way to
  integrate it on django's admin. Note from `@spookylukey
  <https://github.com/spookylukey>`_: There is a `really easy way
  <https://docs.djangoproject.com/en/1.11/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fieldsets>`_ to put the fields
  side-by-side in the django's contrib admin.
* ``Select2`` for selects with fk, etc... I've tried
  ``django-select2`` + ``django-easy-select2`` with not too much luck (I'm sure
  it was my fault), didn't know ``django-autocomplete-light`` tbh.
* Lots of widgets depending on the type of field (44+ field types: date, time,
  datetime, toggle, video...).
* Lots of columns - the field representation in a listing table - (images,
  data with/without link, buttons, extra buttons...).
* Reordering - nested sortable - (something similar to ``django-mptt``)...

After seeing all that stuff I felt a bit shocked, started to look for something
similar for django (for the built-in admin or some other piece of code that
gives me something closer). I've tried django-material, django-jet, grappelli,
django-adminlte2, djadmin, django-flat-responsive... but in the end I felt that
only a cocktail with some of them could do the job. I did a list of soft and
features (similar to the above's one) and, in the end, I've started to think
that if I had that need, why not to make it public and test if the community
feels same "lacks" than me?. That's the story behind this project.

Crazy? yep, I felt myself really weird after read Jacob's post
(https://jacobian.org/writing/so-you-want-a-new-admin/) but I needed to make
the project public.

.. _features:

Features
========

* Responsive design: django-adminlte2
* Tabbed forms: django-crispy-forms
* Wrappable fields: django-crispy-forms
* Image cropping: django-image-cropping (custom widget)
* something for select2 (custom widget)
* something for other file types (upload, multiple upload, date, time, color
  etc...) (custom widgets)
* Reordering: django-mptt
* Easy to understand/adapt: A cruds mixin with CBV was a good idea, I've
  found https://github.com/bmihelac/django-cruds and it rang the definitely
  bell here
* Easy to extend (anyone could contribute with new widgets or behaviors,
  inlines, search, filters...)

.. _onlineresources:

Online Resources
================

* `Code repository`_
* `Documentation`_
* `Pypi`_
* `DjangoPackages`_
* For reporting a bug use `GitHub Issues`_


Screenshots
===========

.. image:: https://raw.githubusercontent.com/oscarmlage/django-cruds-adminlte/master/docs/images/cruds-list.png
    :target: https://raw.githubusercontent.com/oscarmlage/django-cruds-adminlte/master/docs/images/cruds-list.png

.. image:: https://raw.githubusercontent.com/oscarmlage/django-cruds-adminlte/master/docs/images/cruds-select2.png
    :target: https://raw.githubusercontent.com/oscarmlage/django-cruds-adminlte/master/docs/images/cruds-select2.png

.. image:: https://raw.githubusercontent.com/oscarmlage/django-cruds-adminlte/master/docs/images/cruds-tabs.png
    :target: https://raw.githubusercontent.com/oscarmlage/django-cruds-adminlte/master/docs/images/cruds-tabs.png

.. image:: https://raw.githubusercontent.com/oscarmlage/django-cruds-adminlte/master/docs/images/cruds-cropping.png
    :target: https://raw.githubusercontent.com/oscarmlage/django-cruds-adminlte/master/docs/images/cruds-cropping.png

.. image:: https://raw.githubusercontent.com/oscarmlage/django-cruds-adminlte/master/docs/images/cruds-inlines.png
    :target: https://raw.githubusercontent.com/oscarmlage/django-cruds-adminlte/master/docs/images/cruds-inlines.png

.. image:: https://raw.githubusercontent.com/oscarmlage/django-cruds-adminlte/master/docs/images/cruds-ckeditor.png
    :target: https://raw.githubusercontent.com/oscarmlage/django-cruds-adminlte/master/docs/images/cruds-ckeditor.png

.. image:: https://raw.githubusercontent.com/oscarmlage/django-cruds-adminlte/master/docs/images/cruds-custom-sidebar.png
    :target: https://raw.githubusercontent.com/oscarmlage/django-cruds-adminlte/master/docs/images/cruds-custom-sidebar.png

.. image:: https://raw.githubusercontent.com/oscarmlage/django-cruds-adminlte/master/docs/images/cruds-responsive.png
    :target: https://raw.githubusercontent.com/oscarmlage/django-cruds-adminlte/master/docs/images/cruds-responsive.png


.. _`Code repository`: https://github.com/oscarmlage/django-cruds-adminlte
.. _`Documentation`: http://django-cruds-adminlte.readthedocs.io/
.. _`Pypi`: https://pypi.python.org/pypi/django-cruds-adminlte/
.. _`GitHub Issues`: https://github.com/oscarmlage/django-cruds-adminlte/issues/
.. _`DjangoPackages`: https://djangopackages.org/packages/p/cruds/

