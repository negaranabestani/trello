from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from dto_utils.response import BaseResponseDTO
from dto_utils.serilizer import ResponseDtoSerializer
from .models import Role
from user.models import TrelloUser
from user.serializers import TrelloUserSerializer, TrelloUserResponseSerializer
from .serializers import RoleResponseSerializer, RoleSerializer


class CreateRoleOrWorkspaceListUsers(generics.ListAPIView, generics.CreateAPIView):
    serializer_class = RoleSerializer

    def list(self, request, *args, **kwargs):
        self.queryset = Role.objects.filter(workspace=self.kwargs.get('workspace')).values_list("user", flat=True)
        uids = self.filter_queryset(self.get_queryset())
        queryset = TrelloUser.objects.filter(pk__in=set(uids))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TrelloUserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TrelloUserSerializer(queryset, many=True)
        data = serializer.data
        response = TrelloUserResponseSerializer(data, "successful").data
        return Response(data=response, status=200)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = RoleResponseSerializer(serializer.data, "successful").data
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)


class RoleUpdateDelete(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    # API endpoint that returns a single customer by pk.
    serializer_class = RoleSerializer
    lookup_field = 'user'
    def update(self, request, *args, **kwargs):
        self.queryset = Role.objects.filter(workspace=self.kwargs.get('workspace'))
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        response = RoleResponseSerializer(serializer.data, "successful").data
        return Response(data=response, status=200)

    def destroy(self, request, *args, **kwargs):
        self.queryset = Role.objects.filter(workspace=self.kwargs.get('workspace'))
        print('delete')
        instance = self.get_object()
        self.perform_destroy(instance)
        response = ResponseDtoSerializer(BaseResponseDTO("successful delete")).data
        return Response(data=response, status=200)
