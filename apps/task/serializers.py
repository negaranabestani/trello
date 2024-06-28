from rest_framework import serializers
from .models import Task, SubTask


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        read_only_fields = ['id', 'created_at', 'updated_at']
        fields = "__all__"


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        read_only_fields = ['id', 'created_at', 'updated_at']
        fields = "__all__"
