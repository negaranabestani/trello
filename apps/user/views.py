from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import TrelloUserSerializer, TrelloUserAuthSerializer, TrelloUserAuthResponseSerializer, \
    TrelloUserResponseSerializer,TrelloUserLogInSerializer
from dto_utils.response import BaseResponseDTO
from dto_utils.serilizer import ResponseDtoSerializer


# Create your views here.

class LoginView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = TrelloUserLogInSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(
            username=username, password=password)
        if user is None:
            response = ResponseDtoSerializer(BaseResponseDTO("invalid username or password")).data
            return Response(data=response, status=401)

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        response = TrelloUserAuthResponseSerializer(str(refresh), access, user, "successful").data
        return Response(data=response, status=200)


class TrelloUserCreate(generics.CreateAPIView):
    serializer_class = TrelloUserAuthSerializer

    def create(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(data.get("password"))
            user.save()
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            response = TrelloUserAuthResponseSerializer(str(refresh), access, user, "successful").data
            return Response(data=response, status=200)


class TrelloUserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = TrelloUserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        response = TrelloUserResponseSerializer(data, "successful").data
        return Response(data=response, status=200)


class TrelloUserDetailUpdateDelete(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    # API endpoint that returns a single customer by pk.
    queryset = User.objects.all()
    serializer_class = TrelloUserSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        response = TrelloUserResponseSerializer(serializer.data, "successful").data
        return Response(data=response, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        print('delete')
        instance = request.user
        self.perform_destroy(instance)
        response = ResponseDtoSerializer(BaseResponseDTO("successful delete")).data
        return Response(data=response, status=200)

    def retrieve(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance)
        response = TrelloUserResponseSerializer(serializer.data, "successful").data
        return Response(data=response, status=200)