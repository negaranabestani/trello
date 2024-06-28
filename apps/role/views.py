from rest_framework.viewsets import ModelViewSet

from .models import Role, UserWorkspaceRole
from .serializers import RoleSerializer, UserWorkspaceRoleSerializer


class RoleViewSet(ModelViewSet):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()


class UserWorkspaceRoleViewSet(ModelViewSet):
    serializer_class = UserWorkspaceRoleSerializer
    queryset = UserWorkspaceRole.objects.all()
