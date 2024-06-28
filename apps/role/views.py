from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from core.exceptios import TrelloException
from core.viewsets import BaseViewSet
from user.serializers import UserSerializer
from .models import Role, UserWorkspaceRole
from .serializers import RoleSerializer, UserWorkspaceRoleSerializer


class RoleViewSet(BaseViewSet):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()


class UserWorkspaceRoleViewSet(BaseViewSet):
    serializer_class = UserWorkspaceRoleSerializer
    queryset = UserWorkspaceRole.objects.all()

    def check_permissions(self, request):
        # check user permission to access that workspace and to be the Admin
        super(UserWorkspaceRoleViewSet, self).check_permissions(request)
        if not UserWorkspaceRole.objects.filter(workspace_id=self.kwargs["workspace"], user_id=self.request.user.id, role="Admin").exists():
            raise TrelloException("شما دسترسی کافی برای ایجاد تغییرات در این ورک اسپیس را ندارید.", 403)

        request.data["workspace"] = self.kwargs["workspace"]
        if request.method in ["PUT", "PATCH", "DELETE"]:
            request.data["user"] = self.kwargs["pk"]

    def get_queryset(self):
        # filtering tasks based on workspace
        return UserWorkspaceRole.objects.filter(workspace_id=self.kwargs["workspace"])

    def get_object(self):
        return get_object_or_404(self.get_queryset(), user_id=self.kwargs["pk"])

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).select_related("user")
        data = []

        for i in queryset:
            serializer = UserSerializer(i.user)
            data.append({
                **serializer.data,
                "role": i.role
            })

        return Response(data)
