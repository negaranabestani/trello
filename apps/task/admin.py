from django.contrib import admin

# Register your models here.
from task.models import SubTask, Task

admin.site.register(Task)
admin.site.register(SubTask)
