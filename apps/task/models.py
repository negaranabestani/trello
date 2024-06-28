from django.db import models


class Task(models.Model):
    PLANNED = 'Planned'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'

    STATUSES = (
        (PLANNED, PLANNED),
        (IN_PROGRESS, IN_PROGRESS),
        (COMPLETED, COMPLETED)
    )

    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    Priorities = (
        (LOW, LOW),
        (MEDIUM, MEDIUM),
        (HIGH, HIGH)
    )

    # fields
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=60, blank=True, null=True)
    status = models.CharField(max_length=16, choices=STATUSES)
    estimated_time = models.TimeField(null=True, blank=True)
    actual_time = models.TimeField(null=True, blank=True)
    priority = models.CharField(max_length=8, choices=Priorities, null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    image_url = models.ImageField(null=True, blank=True)

    # fk
    workspace = models.ForeignKey("workspace.Workspace", on_delete=models.CASCADE)
    assignee = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True, blank=True)

    # log
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}: {self.title} | {self.workspace.name} | {self.assignee.name if self.assignee_id else ''}"


class SubTask(models.Model):
    # fields
    title = models.CharField(max_length=20)
    is_completed = models.BooleanField(default=False)

    # fk
    task = models.ForeignKey("task.Task", on_delete=models.CASCADE)
    assignee = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True, blank=True)

    # log
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}: {self.title} | {self.task.title} | {self.assignee.name if self.assignee_id else ''}"
