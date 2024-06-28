from rest_framework.viewsets import ModelViewSet

from .models import Workspace
from .serializers import WorkspaceSerializer


class WorkspaceViewSet(ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
