import pytest
from rest_framework.exceptions import ValidationError
from drf_api_action_example.users.faker import UserFactory
# importing fixtures
from drf_api_action_example_tests.fixtures import users_api


def test_get_user_details(users_api):
    user = UserFactory(first_name='shosho', last_name='bobo', age=30)
    assert user
    user_details = users_api.details(pk=user.id)
    assert user_details['first_name'] == user.first_name


def test_add_user(users_api):
    output = users_api.add(first_name='bar', last_name='baz', age=30)
    assert output['id'] is not None


def test_add_user_exception_on_age(users_api):
    with pytest.raises(ValidationError):
        users_api.add(first_name='bar', last_name='baz', age=150)


def test_get_users_by_name(users_api):
    users = []
    for _ in range(10):
        users.append(UserFactory(first_name='bobo').id)

    next_page = 1
    batches = []
    while next_page is not None:
        output = users_api.filter_by_first_name(first_name='bobo', page=next_page)
        batches.extend([user['id'] for user in output['results']])
        if output['next']:
            next_page = int(output['next'].split("=")[1])
        else:
            next_page = None

    assert users == batches
