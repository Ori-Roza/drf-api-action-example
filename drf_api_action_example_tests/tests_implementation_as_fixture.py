import pytest
from rest_framework.exceptions import ValidationError
from drf_api_action_example.tasks.faker import TaskFactory
from drf_api_action_example.tasks.views import TasksViewSet
from drf_api_action.fixtures import action_api


@pytest.mark.action_api(view_set_class=TasksViewSet)
def test_get_task_details(action_api):
    task = TaskFactory()
    task_details = action_api.get_task_details(pk=task.id)
    assert task_details['assigned_by'] == task.assigned_by


@pytest.mark.action_api(view_set_class=TasksViewSet)
def test_add_user(action_api):
    output = action_api.add_task(assigned_by='test', notes='bar baz')
    assert output['id'] is not None


@pytest.mark.action_api(view_set_class=TasksViewSet)
def test_add_task_exception_on_assigned_by(action_api):
    with pytest.raises(ValidationError) as error:
        _ = action_api.add_task(assigned_by='t', notes='bar baz')
    assert "assigned_by must be between 4 and 32 chars" in str(error.value)


@pytest.mark.action_api(view_set_class=TasksViewSet)
def test_get_tasks_by_name(action_api):
    tasks = []
    for i in range(10):
        tasks.append(TaskFactory(assigned_by='bobo', notes=f'notes_{i}').id)

    next_page = 1
    batches = []
    while next_page is not None:
        output = action_api.filter_by_assigned_by(assigned_by='bobo', page=next_page)
        batches.extend([user['id'] for user in output['results']])
        if output['next']:
            next_page = int(output['next'].split("=")[1])
        else:
            next_page = None

    assert tasks == batches
