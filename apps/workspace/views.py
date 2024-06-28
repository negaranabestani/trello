from core.viewsets import BaseViewSet
from .models import Workspace
from .serializers import WorkspaceSerializer


class WorkspaceViewSet(BaseViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer

    def get_queryset(self):
        return Workspace.objects.filter(user_workspace_roles__user_id=self.request.user.id)
