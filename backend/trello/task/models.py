import enum

from django.db import models

from user.models import TrelloUser
from workspace.models import Workspace


class Status(enum.Enum):
    COMPLETED = 'Completed'
    IN_PROGRESS = 'In Progress'
    PLANNED = 'Planned'


class Priority(enum.Enum):
    HIGH = 'High'
    MEDIUM = 'Medium'
    LOW = 'Low'


class Task(models.Model):
    title = models.CharField(max_length=20, blank=False, null=False)
    description = models.CharField(max_length=60, blank=False, null=False)
    status = models.CharField(default=Status.PLANNED)
    estimated_time = models.TimeField()
    actual_time = models.TimeField()
    due_date = models.DateTimeField()
    priority = models.CharField()
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, blank=False, null=False)
    assignee = models.ForeignKey(TrelloUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_url = models.URLField()

    def __str__(self):
        return "{" + f"{self.title},{self.description},{self.created_at},{self.updated_at},{self.status},{self.estimated_time}," \
                     f"{self.actual_time},{self.due_date},{self.priority},{self.workspace},{self.assignee},{self.image_url}" + "}"
