from django.contrib import admin

# Register your models here.
from task.models import SubTask, Task, Comment, Notification

admin.site.register(Task)
admin.site.register(SubTask)
admin.site.register(Comment)
admin.site.register(Notification)
