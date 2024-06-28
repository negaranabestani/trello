from rest_framework import serializers

from core.exceptios import TrelloException
from role.serializers import UserWorkspaceRoleSerializer
from .models import Workspace


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        read_only_fields = ['id', 'created_at', 'updated_at']
        fields = "__all__"

    def create(self, validated_data):
        instance = super(WorkspaceSerializer, self).create(validated_data)

        uwrs = UserWorkspaceRoleSerializer(data={
            "user": self.context["request"].user.id,
            "workspace": instance.id,
            "role": "Admin"
        })

        uwrs.is_valid(raise_exception=True)
        uwrs.save()

        return instance

    def is_valid(self, raise_exception=False):
        if not self.initial_data.get("name", None):
            raise TrelloException("نام اجباری است.")

        if len(self.initial_data.get("name")) < 6:
            raise TrelloException("نام باید حداقل ۶ کاراکتر باشد.")

        super(WorkspaceSerializer, self).is_valid(raise_exception=raise_exception)
