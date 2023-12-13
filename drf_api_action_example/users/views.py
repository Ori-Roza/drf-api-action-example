from rest_framework import mixins, viewsets, status
from drf_api_action.mixins import APIRestMixin
from drf_api_action.decorators import action_api
from rest_framework.response import Response

from drf_api_action_example.users.models import User
from drf_api_action_example.users import serializers


class UsersViewSet(APIRestMixin, mixins.RetrieveModelMixin,
                   mixins.ListModelMixin, viewsets.GenericViewSet):

    serializer_class = serializers.UsersSerializer

    def get_queryset(self):
        return User.objects.all()

    @action_api(detail=True,
                methods=['get'],
                url_path='/',
                url_name='users/',
                serializer_class=serializers.GetUserDetailsSerializer)
    def get_user_details(self, request, **kwargs):
        """
        returns user details, pk expected
        """
        serializer = self.get_serializer(instance=self.get_object())
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action_api(detail=False,
                methods=['post'],
                url_path='/',
                url_name='users/',
                serializer_class=serializers.AddUserSerializer)
    def add_user(self, request, **kwargs):
        """
        adds new user
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action_api(detail=False,
                methods=['get'],
                url_path='/',
                url_name='users/',
                serializer_class=serializers.UsersByFirstNameSerializer)
    def filter_by_first_name(self, request, **kwargs):
        """
        returns users by given first_name
        """
        self.get_serializer(data=request.query_params).is_valid(raise_exception=True)
        users = User.objects.filter(first_name=request.query_params['first_name'])
        page = self.paginate_queryset(users)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
