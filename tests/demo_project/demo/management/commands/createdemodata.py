from django.core.management.base import BaseCommand, CommandError
from demo.factories import UserFactory
from testapp.factories import AuthorFactory


class Command(BaseCommand):
    help = 'Create demo data'

    def handle(self, *args, **options):
        users = {
            'admin': UserFactory.create(username='admin'),
            'john': UserFactory.create(username='john')
        }
        for u in users.values():
            if u.username == 'admin':
                u.is_superuser = True
            u.is_staff = True
            u.set_password('demo')
            u.save()
            self.stdout.write(self.style.SUCCESS("Demo user '%s' with password '%s'" % (u.username, 'demo')))

        authors = AuthorFactory.create_batch(4)

        self.stdout.write(self.style.SUCCESS('Successfully created demo data'))
