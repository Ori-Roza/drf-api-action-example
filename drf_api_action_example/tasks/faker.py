import factory
from drf_api_action_example.tasks.models import Task


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    id = factory.Sequence(int)
    assigned_by = factory.LazyFunction(lambda : f"{factory.Faker('first_name')}_{factory.Faker('last_name')}")
    notes = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur eleifend orci ut accumsan congue.' \
            ' Aliquam vel nisi pretium, mattis turpis vel, malesuada libero. Maecenas mauris urna, mollis a venenatis' \
            ' at, vestibulum sed augue. Nam id ante suscipit leo.'
