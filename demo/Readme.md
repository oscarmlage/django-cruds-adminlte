# Instructions

This directory contains a simple demo application of the functionalities
of the cruds_adminlte package.

The instructions below create a virtualenv inside this directory and installs
cruds_adminlte from the source tree, not from the PyPi package.

## Prepare the environment
```
# From the `demo` directory.
$ python -m venv demo-venv
$ source demo-venv/bin/activate
(demo-venv) $ pip install -r requirements.txt
```

## Run the app
```
$ source demo-venv/bin/activate
(demo-venv)$ ./manage.py migrate
(demo-venv)$ ./manage.py showmigrations
(demo-venv)$ ./manage.py runserver --settings=demo.settings 0.0.0.0:4444
Starting development server at http://0.0.0.0:4444/
Quit the server with CONTROL-C.
```

## Test user

- User: user
- Password: user12345

If it doesn't work create your own credentials:

```
$ source demo-venv/bin/activate
(demo-venv)$ ./manage.py createsuperuser
Username (leave blank to use 'admin'): admin
Email address: ad@min.comm
Password:
Password (again):
Superuser created successfully.
```