from django.db import models

from task.models import Task
from user.models import TrelloUser


class SubTask(models.Model):
    title = models.CharField(max_length=20, blank=False, null=False)
    is_completed = models.BooleanField(default=False)
    assignee = models.ForeignKey(TrelloUser, on_delete=models.SET_NULL, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{" + f"{self.title},{self.created_at},{self.updated_at}" \
                     f"{self.assignee},{self.task}" + "}"
