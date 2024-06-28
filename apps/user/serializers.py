from rest_framework import serializers
from .models import User
from dto_utils.response import BaseResponseDTO
from dto_utils.serilizer import ResponseDtoSerializer
from .responseDTOs import TrelloAuth


class TrelloUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ['created_at', 'updated_at', 'id']
        fields = ['id', 'email', 'username', 'created_at', 'updated_at']


class TrelloUserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']


class TrelloUserLogInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class TrelloAuthSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    access_token = serializers.CharField()


class TrelloUserAuthResponseSerializer:
    def __init__(self, refresh, access, user, message):
        self.auth = TrelloAuthSerializer(TrelloAuth(access, refresh)).data
        self.user = TrelloUserSerializer(user).data
        self.response = ResponseDtoSerializer(BaseResponseDTO(message)).data

    @property
    def data(self):
        return {"response": self.response, "auth": self.auth, "user": self.user}


class TrelloUserResponseSerializer:
    def __init__(self, users, message):
        self.users = users
        self.response = ResponseDtoSerializer(BaseResponseDTO(message)).data

    @property
    def data(self):
        return {"response": self.response, "users": self.users}
