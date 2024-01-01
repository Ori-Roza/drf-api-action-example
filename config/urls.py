from rest_framework import routers
from django.urls import path, include
from drf_api_action_example.users import views as UsersViews
from drf_api_action_example.tasks import views as TasksViews

router = routers.DefaultRouter()
router.register(r'api/users', UsersViews.UsersViewSet, basename='users')
router.register(r'api/tasks', TasksViews.TasksViewSet, basename='tasks')

urlpatterns = [
    path('', include(router))
]