from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.viewsets import BaseViewSet
from .models import User


# Create your views here.
from .serializers import UserSerializer


class UserViewSet(BaseViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        if self.request.method != "GET":
            return User.objects.filter(id=self.request.user.id)
        return User.objects.all()

    @action(methods=["GET", "PUT"], detail=True, url_path="profile")
    def profile(self, request, *args, **kwargs):
        if request.method == "GET":
            return Response(UserSerializer(self.get_object()).data)
        elif request.method == "PUT":
            serializer = UserSerializer(instance=self.get_object(), data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(methods=["GET"], detail=False, url_path="me")
    def me(self, request, *args, **kwargs):
        return Response(UserSerializer(self.request.user).data)


class UserRegistration(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
