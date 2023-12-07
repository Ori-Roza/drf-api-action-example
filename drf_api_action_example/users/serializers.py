from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer, IntegerField, CharField

from drf_api_action_example.users.models import User


class UsersSerializer(Serializer):
    id = IntegerField(read_only=True)
    first_name = CharField(read_only=True, max_length=32)
    last_name = CharField(read_only=True, max_length=32)
    age = IntegerField(read_only=True, max_value=120)

    class Meta:
        model = User
        fields = ("*",)



class GetUserDetailsSerializer(Serializer):
    id = IntegerField(read_only=True)
    first_name = CharField(read_only=True, max_length=32)
    last_name = CharField(read_only=True, max_length=32)
    age = IntegerField(read_only=True, max_value=120)

    class Meta:
        model = User
        fields = ("*", )


class AddUserSerializer(Serializer):
    id = IntegerField(required=False)
    first_name = CharField(required=True, max_length=32)
    last_name = CharField(required=True, max_length=32)
    age = IntegerField(required=False, max_value=120)

    class Meta:
        model = User
        fields = ("*", )

    def validate(self, attrs):
        age = attrs['age']

        if age and age > 120:
            raise ValidationError(detail='age must be between 0 and 120')
        return attrs

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance


class UsersByFirstNameSerializer(Serializer):
    id = IntegerField(read_only=True)
    first_name = CharField(required=True, max_length=32)
    last_name = CharField(read_only=True, max_length=32)
    age = IntegerField(read_only=True, max_value=120)

    class Meta:
        model = User
        fields = ("*",)

    def validate(self, attrs):
        if "first_name" not in attrs:
            raise ValidationError("first_name is required")
        return attrs
