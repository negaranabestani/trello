from django.urls import path
from .views import UpdateDeleteRetrieveSubTask, CreateListSubTasks

urlpatterns = [
    path('tasks/<int:task>/subtasks', CreateListSubTasks.as_view()),
    path('tasks/<int:task>/subtasks/<int:pk>', UpdateDeleteRetrieveSubTask.as_view()),
]
