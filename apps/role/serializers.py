from rest_framework import serializers

from .models import Role, UserWorkspaceRole


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        read_only_fields = ['id', 'created_at', 'updated_at']
        fields = "__all__"


class UserWorkspaceRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWorkspaceRole
        read_only_fields = ['id', 'created_at', 'updated_at']
        fields = "__all__"
