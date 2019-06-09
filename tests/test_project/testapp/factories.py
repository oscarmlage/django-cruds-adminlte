from factory import DjangoModelFactory, Faker

from testapp.models import Author


class AuthorFactory(DjangoModelFactory):
    name = Faker("name")
    birthday = Faker('date_of_birth', tzinfo=None, minimum_age=10, maximum_age=115)

    class Meta:
        model = Author
