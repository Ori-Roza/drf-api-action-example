import pytest

from drf_api_action_example.users.views import UsersViewSet


@pytest.fixture()
def users_api():
    api = UsersViewSet()
    return api
