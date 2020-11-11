============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

There are multiple ways to contribute to an open source project. Not
all is code. You might help with documentation, translations, triaging
issues, helping with the community, ...

We use github for coordinating development efforts. And if you are
looking for ideas on how to help, that's as good as it gets on where
to start.

On github, some issues might be tagged "good first issue", which means
that we believe it is an issue that does not require a deep knowledge
of the library.

Note that issues might be bugs that need fixing, or features to be
implemented. Always read the issue log before doing anything as there
might be proposals on how to handle that particular issue, proposed
implementations, etc.

We do not currently have any user forums.

Useful links:

- Github main repository: https://github.com/oscarmlage/django-cruds-adminlte/

.. contents:: :local:

Report Bugs and propose features
--------------------------------

Report bugs at https://github.com/oscarmlage/django-cruds-adminlte/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.
* Code samples if possible

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Contribute code
---------------

We have an open issue (https://github.com/oscarmlage/django-cruds-adminlte/issues/129)
regarding the code style of the project. Of course, PEP-8 must be respected.

Our test infrastructure uses `pytest`_ and `tox`_ at its core. During normal
development you might want to simply run ``pytest`` which will run the
testsuite with your current python and django versions.

Both options will drop artifacts (reports) into the tests/reports/ folder.

The master branch includes CircleCI configuration, so you can easily run the
full test suite there by properly setting up you account there (the free
limits are quite generous).

.. _pytest: https://pytest.org
.. _tox: https://tox.readthedocs.io/en/latest/

The test suite is composed by a series of fixtures and a test_project that can
be extended to support new test cases.

* `pytest-django`_ fixtures and helpers (pay attention to the django_db
  pytest mark).
* `pytest-selenium`_ fixtures and our `selenium` mark.
* ``admin_browser`` will get you a selenium client already authenticated
  as an admin user.

See the ``conftest.py`` file in the tests folder for more fixtures.

.. _pytest-django: https://pytest-django.readthedocs.io/en/latest/helpers.html
.. _pytest-selenium: https://pytest-selenium.readthedocs.io/en/latest/user_guide.html


Submitting pull requests
~~~~~~~~~~~~~~~~~~~~~~~~

If you decide to go for it and implement some feature or fix a bug,
please consider the following:

- If the code you are about to change is not covered by the test suite,
  please fix that first. Also, do this on a separate PR so it can be merged
  before the "main" thing.

If you are fixing bugs:

- Do not introduce a backwards incompatibility
- Write a test that reproduces de bug. That way we make sure that a) the bug
  can be reproduced, b) it is fixed, c) it does not come back!

If you are implementing new features:

- Make sure you document them
- Consider adding an use case on the demo project to show the feature working
- Keep backwards compatibility in mind
- Discuss with the community the necessity of such feature

Please, make sure you run the full test suite before submitting a PR.
That means that you either run ``tox`` localy or run the CircleCI config
provided.

Write Documentation
-------------------

Documentation is really important. It is what makes it possible to understand
how things work. Or how things are supposed to work. You can help by:

- Adding docstrings where needed
- Fixing discrepancies between docstrings or sphinx docs (the ones
  in .rst format)
- Write articles, blog posts, ...
- Detect misbehaviours: when the documentation says something, and the
  code does another thing. Please file bugs on those.
