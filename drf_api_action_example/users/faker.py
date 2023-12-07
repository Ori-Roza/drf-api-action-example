import random

import factory
from drf_api_action_example.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    id = factory.Sequence(int)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    age = factory.LazyFunction(lambda: random.randint(0, 120))


