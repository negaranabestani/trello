from django.db.models.signals import post_save

from task.models import Task, Notification


def handle_notification(sender, instance: Task, created, **kwargs):
    if created and instance.assignee_id:
        Notification.objects.create(
            title=f"Task {instance.title} has been created and assigned to you.",
            receiver_id=instance.assignee_id
        )
    elif len(instance.subscribers) > 0:
        for user_id in instance.subscribers:
            Notification.objects.create(
                title=f"Task {instance.title} has been updated.",
                receiver_id=user_id
            )


post_save.connect(Task, handle_notification, dispatch_uid="creat_notification")
