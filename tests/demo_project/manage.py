#!/usr/bin/env python
import os
import sys
from pathlib import Path

if __name__ == "__main__":
    # We add ourselves into the python path, so we can find
    # the package later.
    demo_root =os.path.dirname(os.path.abspath(__file__))
    crud_install = os.path.dirname(os.path.dirname(demo_root))

    sys.path.insert(0, crud_install)
    os.chdir(demo_root)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
