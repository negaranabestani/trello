from rest_framework.viewsets import ModelViewSet

from .models import Task, SubTask
from .serializers import TaskSerializer, SubTaskSerializer


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class SubTaskViewSet(ModelViewSet):
    serializer_class = SubTaskSerializer
    queryset = SubTask.objects.all()
