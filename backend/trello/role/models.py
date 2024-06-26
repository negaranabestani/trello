import enum

from django.db import models
from workspace.models import Workspace
from user.models import TrelloUser


class UserRole(enum.Enum):
    Admin = 'Admin'
    Standard_User = 'StandardUser'


class Role(models.Model):
    role = models.CharField(default=UserRole.Standard_User)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey(TrelloUser, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{" + f"{self.role},{self.user},{self.workspace},{self.created_at},{self.updated_at}" + "}"
