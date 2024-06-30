from core.exceptios import TrelloException
from core.viewsets import BaseViewSet
from role.models import UserWorkspaceRole
from .models import Task, SubTask
from .serializers import TaskSerializer, SubTaskSerializer


class TaskViewSet(BaseViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def check_permissions(self, request):
        # check user permission to access that workspace
        super(TaskViewSet, self).check_permissions(request)
        if not UserWorkspaceRole.objects.filter(workspace_id=self.kwargs["workspace"], user_id=self.request.user.id).exists():
            raise TrelloException("شما به این ورک اسپیس دسترسی ندارید.", 403)

        request.data["workspace"] = self.kwargs["workspace"]

    def get_queryset(self):
        # filtering tasks based on workspace
        return Task.objects.filter(workspace_id=self.kwargs["workspace"])


class SubTaskViewSet(BaseViewSet):
    serializer_class = SubTaskSerializer
    queryset = SubTask.objects.all()

    def check_permissions(self, request):
        # check user permission to access that workspace
        super(SubTaskViewSet, self).check_permissions(request)
        if not Task.objects.filter(id=self.kwargs["task"]).exists():
            raise TrelloException("تسک وجود ندارد.")

        task = Task.objects.get(id=self.kwargs["task"])

        if not UserWorkspaceRole.objects.filter(workspace_id=task.workspace_id, user_id=self.request.user.id).exists():
            raise TrelloException("شما به این ورک اسپیس دسترسی ندارید.", 403)

        request.data["task"] = self.kwargs["task"]

    def get_queryset(self):
        # filtering tasks based on workspace
        return SubTask.objects.filter(task_id=self.kwargs["task"])