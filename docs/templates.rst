==========================
Templates and templatetags
==========================


.. _templates:

Templates
=========

django-cruds-adminlte views will append CRUD template name to a list of default
candidate template names for given action.

CRUD Templates are::

    cruds/create.html
    cruds/delete.html
    cruds/detail.html
    cruds/list.html
    cruds/update.html

Templates are based in `AdminLTE2 <https://almsaeedstudio.com/themes/AdminLTE/index2.html>`_
and `django-adminlte2 <https://github.com/adamcharnock/django-adminlte2>`_ (but
this last is not required because the templates are included in this project).
They're ready to run with:

* `django-crispy-forms <https://django-crispy-forms.readthedocs.io/en/latest/>`_
* `select2 <https://select2.github.io/>`_
* `django-cropping-image <https://github.com/jonasundderwolf/django-image-cropping>`_

If you want to override the sidebar you can do it creating a file called
``templates/adminlte/lib/_main_sidebar.html`` inside your project and you can
put there the contents you want.


.. _templatetags:

Templatetags
============

``crud_fields`` templatetag displays fields for an object::

    {% load crud_tags %}

    <table class="table">
      <tbody>
        {% crud_fields object "name, description" %}
      </tbody>
    </table>

Use ``cruds_adminlte.util.crud_url`` shortcut function to quickly get url for
instance for given action::

    crud_url(author, 'update')

Is same as::

        reverse('testapp_author_update', kwargs={'pk': author.pk})
