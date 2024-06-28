from rest_framework import generics, status
from rest_framework.response import Response

from dto_utils.response import BaseResponseDTO
from dto_utils.serilizer import ResponseDtoSerializer
from user.serializers import TrelloUserSerializer
from .models import Task
from .serializers import TaskSerializer, TaskResponseSerializer


class CreateListTasks(generics.ListAPIView, generics.CreateAPIView):
    serializer_class = TaskSerializer

    def list(self, request, *args, **kwargs):
        self.queryset = Task.objects.filter(workspace=self.kwargs.get('workspace'))
        page = self.paginate_queryset(self.get_queryset())
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.get_queryset(), many=True)
        data = serializer.data
        response = TaskResponseSerializer(data, "successful").data
        return Response(data=response, status=200)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(kwargs=kwargs, raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = TaskResponseSerializer(serializer.data, "successful").data
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)


class UpdateDeleteRetrieveTask(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    # API endpoint that returns a single customer by pk.
    serializer_class = TaskSerializer

    def update(self, request, *args, **kwargs):
        self.queryset = Task.objects.filter(workspace=self.kwargs.get('workspace'))
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        response = TaskResponseSerializer(serializer.data, "successful").data
        return Response(data=response, status=200)

    def destroy(self, request, *args, **kwargs):
        self.queryset = Task.objects.filter(workspace=self.kwargs.get('workspace'))
        instance = self.get_object()
        self.perform_destroy(instance)
        response = ResponseDtoSerializer(BaseResponseDTO("successful delete")).data
        return Response(data=response, status=200)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response = TaskResponseSerializer(serializer.data, "successful").data
        return Response(data=response, status=200)
