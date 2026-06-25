from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'completed', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class UserSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'display_name', 'city', 'phone_number')
