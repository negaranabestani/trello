import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save

from task.models import Task, Notification
from task.serializers import NotificationSerializer


def handle_notification(sender, instance: Task, created, **kwargs):
    if created and instance.assignee_id:
        Notification.objects.create(
            title=f"Task {instance.title} has been created and assigned to you.",
            receiver_id=instance.assignee_id,
            task_id=instance.id
        )
    elif len(instance.subscribers) > 0:
        for user_id in instance.subscribers:
            Notification.objects.create(
                title=f"Task {instance.title} has been updated.",
                receiver_id=user_id,
                task_id=instance.id
            )


def send_notification(sender, instance: Notification, created, **kwargs):
    if created:
        serializer = NotificationSerializer(instance=instance)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'user_{instance.receiver_id}',
            {
                'type': 'send_message',
                'message': json.dumps(serializer.data)
            }
        )


post_save.connect(handle_notification, sender=Task, dispatch_uid="create_notification")
post_save.connect(send_notification, sender=Notification, dispatch_uid="send_notification")
