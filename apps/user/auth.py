from django.contrib.auth.backends import ModelBackend, BaseBackend
from rest_framework.request import Request


class CustomJWTBackend(BaseBackend):
    def authenticate(self, request, **kwargs):
        print(kwargs.get('pk'))
        print(request.user.id)
        if kwargs.get('pk') != request.user.id:
            return None
        return request.user
