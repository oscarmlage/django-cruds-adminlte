======================
Demo / testing project
======================

A full demonstration project is included with django-cruds-adminlte's
which you can use as a companion "cookbook". The project is used intensively
for the testsuite and/or to generate screenshots for the documentation.

You might find the demo project in the `tests/test_project`
folder of the source tree.

.. contents:: :local:

Prepare the environment
-----------------------

The demo project can be run using the same python environment used for
development as it's dependencies are the same.

If you have not setup such environment you can either:

- Refer to the contributing documentation.
- Setup the environment as detailed here.

The main difference is that the detailed instructions on the
contributing documentation are meant for proper development,
testing and patch submission. The instructions here are meant
as a quick solution to run the demo.

.. code-block:: bash

    # From the root directory of the project
    # (the one with a setup.py file).
    $ python -m venv .venv
    $ source .venv/bin/activate
    (venv) $ pip install -r requirements-test.txt

Do not forget to enable the virtual environment when using the demo

.. code-block:: bash

    $ source .venv/bin/activate
    (venv) $

Run the demo
------------

The demo is, pretty much, a standard django project so you can run
it like you would run any other project:

.. code-block:: bash

    (venv)$ ./tests/demo_project/manage.py migrate
    (venv)$ ./tests/demo_project/manage.py showmigrations
    (venv)$ ./tests/demo_project/manage.py runserver --settings=demo_project.settings 0.0.0.0:4444
    Starting development server at http://0.0.0.0:4444/
    Quit the server with CONTROL-C.

Test user
---------

If you want to make the most of the demo, you should really
create a test user to access it.

.. code-block:: bash

    (venv)$ ./tests/demo_project/manage.py createsuperuser
    Username (leave blank to use 'admin'): admin
    Email address: admin@example.comm
    Password:
    Password (again):
    Superuser created successfully.
