from rest_framework import generics, status
from rest_framework.response import Response

from dto_utils.response import BaseResponseDTO
from dto_utils.serilizer import ResponseDtoSerializer
from .models import Workspace
from .serializers import WorkspaceResponseSerializer, WorkspaceSerializer


class WorkspaceCreateList(generics.ListAPIView, generics.CreateAPIView):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            response = WorkspaceResponseSerializer(serializer.data, "successful").data
            return Response(response, status=status.HTTP_201_CREATED, headers=headers)
        response = ResponseDtoSerializer(
            BaseResponseDTO(f"unsuccessful,request: {request.data},error:{serializer._errors}")).data
        return Response(data=response, status=200)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        response = WorkspaceResponseSerializer(data, "successful").data
        return Response(data=response, status=200)


class WorkspaceDetailUpdateDelete(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView
                                  ):
    # API endpoint that returns a single customer by pk.
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
    
            response = WorkspaceResponseSerializer(serializer.data, "successful").data
            return Response(data=response, status=200)
        response = ResponseDtoSerializer(
            BaseResponseDTO(f"unsuccessful,request: {request.data},error:{serializer._errors}")).data
        return Response(data=response, status=200)

    def destroy(self, request, *args, **kwargs):
        print('delete')
        instance = self.get_object()
        self.perform_destroy(instance)
        response = ResponseDtoSerializer(BaseResponseDTO("successful delete")).data
        return Response(data=response, status=200)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response = WorkspaceResponseSerializer(serializer.data, "successful").data
        return Response(data=response, status=200)
