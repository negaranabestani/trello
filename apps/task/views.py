from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

from core.exceptios import TrelloException
from core.pagination import TrelloPagination
from core.viewsets import BaseViewSet
from role.models import UserWorkspaceRole
from .models import Task, SubTask, Comment, Notification
from .serializers import TaskSerializer, SubTaskSerializer, CommentSerializer, NotificationSerializer


class TaskViewSet(BaseViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    pagination_class = TrelloPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['assignee']

    def check_permissions(self, request):
        # check user permission to access that workspace
        super(TaskViewSet, self).check_permissions(request)
        if not UserWorkspaceRole.objects.filter(workspace_id=self.kwargs["workspace"], user_id=self.request.user.id).exists():
            raise TrelloException("شما به این ورک اسپیس دسترسی ندارید.", 403)

        request.data["workspace"] = self.kwargs["workspace"]

    def get_queryset(self):
        # filtering tasks based on workspace
        return Task.objects.filter(workspace_id=self.kwargs.get("workspace", -1))

    @action(methods=["POST"], detail=True, url_path="watch")
    def watch(self, request, *args, **kwargs):
        task: Task = self.get_object()
        if self.request.user.id not in task.subscribers:
            task.subscribers.append(self.request.user.id)
            task.save()
        return Response({"status": "OK"})

    @action(methods=["POST"], detail=True, url_path="unwatch")
    def unwatch(self, request, *args, **kwargs):
        task: Task = self.get_object()
        if self.request.user.id in task.subscribers:
            task.subscribers.remove(self.request.user.id)
            task.save()
        return Response({"status": "OK"})


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
        return SubTask.objects.filter(task_id=self.kwargs.get("task", -1))


class CommentViewSet(BaseViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def check_permissions(self, request):
        # check user permission to access that workspace
        super(CommentViewSet, self).check_permissions(request)
        if not Task.objects.filter(id=self.kwargs["task"]).exists():
            raise TrelloException("تسک وجود ندارد.")

        task = Task.objects.get(id=self.kwargs["task"])

        if not UserWorkspaceRole.objects.filter(workspace_id=task.workspace_id, user_id=self.request.user.id).exists():
            raise TrelloException("شما به این ورک اسپیس دسترسی ندارید.", 403)

        request.data["task"] = self.kwargs["task"]

    def get_queryset(self):
        # filtering tasks based on workspace
        return Comment.objects.filter(task_id=self.kwargs.get("task", -1))


class NotificationViewSet(BaseViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    def get_queryset(self):
        # filtering tasks based on workspace
        return Notification.objects.filter(receiver_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        raise TrelloException("You can't create a notification.", 403)

    def update(self, request, *args, **kwargs):
        raise TrelloException("You can't update a notification.", 403)

    def destroy(self, request, *args, **kwargs):
        raise TrelloException("You can't remove a notification.", 403)

    @action(methods=["POST"], detail=True, url_path="seen")
    def seen(self, request, *args, **kwargs):
        instance: Notification = self.get_object()
        instance.seen = True
        instance.save()
        return instance
