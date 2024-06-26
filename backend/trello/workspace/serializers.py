from rest_framework import serializers
from dto_utils.response import BaseResponseDTO
from dto_utils.serilizer import ResponseDtoSerializer
from .models import Workspace


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        read_only_fields = ['created_at', 'updated_at', 'id']
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']


class WorkspaceResponseSerializer:
    def __init__(self, workspaces, message):
        self.workspaces = workspaces
        self.response = ResponseDtoSerializer(BaseResponseDTO(message)).data

    @property
    def data(self):
        return {"response": self.response, "workspaces": self.workspaces}
