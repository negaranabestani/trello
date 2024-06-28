from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ['created_at', 'updated_at', 'id']
        fields = "__all__"
