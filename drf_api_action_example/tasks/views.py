from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_api_action_example.tasks.models import Task
from drf_api_action_example.tasks import serializers


class TasksViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.TasksSerializer

    def get_queryset(self):
        return Task.objects.all()

    @action(detail=True,
            methods=['get'],
            url_path='/',
            url_name='tasks/',
            serializer_class=serializers.GetTaskDetailsSerializer)
    def get_task_details(self, request, **kwargs):
        """
        returns task details, pk expected
        """
        serializer = self.get_serializer(instance=self.get_object())
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False,
            methods=['post'],
            url_path='/',
            url_name='tasks/',
            serializer_class=serializers.AddTaskSerializer)
    def add_task(self, request, **kwargs):
        """
        adds new task
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False,
            methods=['get'],
            url_path='/',
            url_name='tasks/',
            serializer_class=serializers.TasksByAssignedBySerializer)
    def filter_by_assigned_by(self, request, **kwargs):
        """
        returns tasks by given assigned_by
        """
        self.get_serializer(data=request.query_params).is_valid(raise_exception=True)
        users = Task.objects.filter(assigned_by=request.query_params['assigned_by'])
        page = self.paginate_queryset(users)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
