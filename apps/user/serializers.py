from rest_framework import serializers

from core.exceptios import TrelloException
from core.serializers import Base64ImageField
from .models import User


class UserSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True, allow_null=True)

    class Meta:
        model = User
        read_only_fields = ['created_at', 'updated_at', 'id']
        exclude = ["password"]

    def is_valid(self, raise_exception=False):
        if not self.initial_data.get("username", None):
            raise TrelloException("نام کاربری نمیتواند خالی باشد.", code=400)

        if not self.initial_data.get("email", None):
            raise TrelloException("ایمیل نمیتواند خالی باشد.", code=400)

        if User.objects.filter(username=self.initial_data.get("username")).exists():
            raise TrelloException("نام کاربری تکراری است.", code=400)

        if User.objects.filter(email=self.initial_data.get("email")).exists():
            raise TrelloException("ایمیل تکراری است.")
        
        return super(UserSerializer, self).is_valid(raise_exception=raise_exception)
