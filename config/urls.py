from rest_framework import routers
from django.urls import path, include
from drf_api_action_example.users import views

router = routers.DefaultRouter()
router.register(r'api/users', views.UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router))
]