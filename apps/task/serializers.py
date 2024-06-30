from rest_framework import serializers

from core.exceptios import TrelloException
from core.serializers import Base64ImageField
from role.models import UserWorkspaceRole
from .models import Task, SubTask, Comment


class TaskSerializer(serializers.ModelSerializer):
    image_url = Base64ImageField(max_length=None, use_url=True, allow_null=True)

    class Meta:
        model = Task
        read_only_fields = ['id', 'created_at', 'updated_at']
        fields = "__all__"

    def is_valid(self, raise_exception=False):
        if not self.initial_data.get("title", None):
            raise TrelloException("عنوان نمیتواند خالی باشد.")

        if (assignee := self.initial_data.get("assignee", None)) and not UserWorkspaceRole.objects.filter(workspace_id=self.initial_data["workspace"], user_id=assignee).exists():
            raise TrelloException("ابتدا کاربر را به ورک اسپیس اضافه کنید.")

        super(TaskSerializer, self).is_valid(raise_exception=raise_exception)


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        read_only_fields = ['id', 'created_at', 'updated_at']
        fields = "__all__"

    def is_valid(self, raise_exception=False):
        if not self.initial_data.get("title", None):
            raise TrelloException("عنوان نمیتواند خالی باشد.")
        task = Task.objects.get(id=self.initial_data["task"])

        if (assignee := self.initial_data.get("assignee", None)) and not UserWorkspaceRole.objects.filter(workspace_id=task.workspace_id, user_id=assignee).exists():
            raise TrelloException("ابتدا کاربر را به ورک اسپیس اضافه کنید.")

        super(SubTaskSerializer, self).is_valid(raise_exception=raise_exception)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        read_only_fields = ['id', 'created_at', 'updated_at']
        fields = "__all__"

    def is_valid(self, raise_exception=False):
        if not self.initial_data.get("content", None):
            raise TrelloException("متن نمیتواند خالی باشد.")

        super(CommentSerializer, self).is_valid(raise_exception=raise_exception)
