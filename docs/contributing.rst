============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/oscarmlage/django-cruds-adminlte/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

django-cruds-adminlte could always use more documentation, whether as part of
the official django-cruds-adminlte docs, in docstrings, or even on the web in
blog posts, articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/oscarmlage/django-cruds-adminlte/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)


Development tips
----------------

django-cruds-adminlte uses `pytest`_ and `tox`_ as the basis of it's tests
infrastructure. During normal development you might want to simply run ``pytest``
which will run the testsuite with your current python and django versions.

But, never forget to run ``tox`` before creating a pull-request to ensure that
your patches work properly in all supported version combinations (refer to the
``tox.ini`` file in the repository for an up-to-date matrix of versions).

Both options will drop artifacts (reports) into the tests/reports/ folder.

.. _pytest: https://pytest.org
.. _tox: https://tox.readthedocs.io/en/latest/

The test suite is composed by a series of fixtures and a test_project that can be
extended to support new test cases.

pytest Fixtures
~~~~~~~~~~~~~~~

First, you have the fixtures of the pytest plugins that are installed, specially:

* `pytest-django`_ fixtures and helpers (pay attention to the django_db pytest mark).
* `pytest-selenium`_.

.. _pytest-django: https://pytest-django.readthedocs.io/en/latest/helpers.html
.. _pytest-selenium: https://pytest-selenium.readthedocs.io/en/latest/user_guide.html

Our conftest.py also provides some fixtures for convenience:

*  ``admin_browser`` will get you a selenium client already authenticated as an admin user.

See the ``conftest.py`` file in the tests folder for more fixtures.
