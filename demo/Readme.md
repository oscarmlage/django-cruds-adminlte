# Instructions

## How to run the app

```
$ virtualenv demo
$ ./demo/bin/activate
(demo)$ pip install -r requirements.txt
(demo)$ ./manage.py migrate
(demo)$ ./manage.py showmigrations
(demo)$ ./manage.py runserver --settings=demo.settings 0.0.0.0:4444
Starting development server at http://0.0.0.0:4444/
Quit the server with CONTROL-C.
```

## Test user

- User: user
- Password: user12345

If it doesn't work create your own credentials:

```
(demo)$ ./manage.py createsuperuser
Username (leave blank to use 'admin'): admin
Email address: ad@min.comm
Password:
Password (again):
Superuser created successfully.
```