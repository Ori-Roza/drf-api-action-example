from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer, IntegerField, CharField

from drf_api_action_example.tasks.models import Task


class TasksSerializer(Serializer):
    id = IntegerField(read_only=True)
    assigned_by = CharField(read_only=True, max_length=32)
    notes = CharField(read_only=True, max_length=256)

    class Meta:
        model = True
        fields = ("*",)


class GetTaskDetailsSerializer(Serializer):
    id = IntegerField(read_only=True)
    assigned_by = CharField(read_only=True, max_length=32)
    notes = CharField(read_only=True, max_length=256)

    class Meta:
        model = Task
        fields = ("*", )


class AddTaskSerializer(Serializer):
    id = IntegerField(required=False)
    assigned_by = CharField(max_length=32)
    notes = CharField(max_length=256)

    class Meta:
        model = Task
        fields = ("*", )

    def validate(self, attrs):
        assigned_by = attrs['assigned_by']

        if assigned_by and len(assigned_by) < 3:
            raise ValidationError(detail='assigned_by must be between 4 and 32 chars')
        return attrs

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance


class TasksByAssignedBySerializer(Serializer):
    id = IntegerField(read_only=True)
    assigned_by = CharField(required=True, max_length=32)
    notes = CharField(read_only=True, max_length=256)

    class Meta:
        model = Task
        fields = ("*",)

    def validate(self, attrs):
        if "assigned_by" not in attrs:
            raise ValidationError("assigned_by is required")
        return attrs
