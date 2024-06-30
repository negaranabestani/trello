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
    status = models.CharField(max_length=16, choices=STATUSES, default=PLANNED)
    estimated_time = models.PositiveSmallIntegerField(null=True, blank=True)
    actual_time = models.TimeField(null=True, blank=True)
    priority = models.CharField(max_length=8, choices=Priorities, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    image_url = models.ImageField(null=True, blank=True)
    subscribers = models.JSONField(default=list, blank=True)

    # fk
    workspace = models.ForeignKey("workspace.Workspace", on_delete=models.CASCADE, related_name="tasks")
    assignee = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")

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
    task = models.ForeignKey("task.Task", on_delete=models.CASCADE, related_name="sub_tasks")
    assignee = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="sub_tasks")

    # log
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}: {self.title} | {self.task.title} | {self.assignee.name if self.assignee_id else ''}"


class Comment(models.Model):
    # fields
    content = models.TextField()

    # fk
    task = models.ForeignKey("task.Task", on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="comments")

    # log
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Notification(models.Model):
    # fields
    title = models.CharField(max_length=512)
    seen = models.BooleanField(default=False)

    # fk
    receiver = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="notifications")
    task = models.ForeignKey("task.Task", on_delete=models.CASCADE, related_name="notifications")

    # log
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
