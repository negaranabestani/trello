from django.urls import path
from .views import UpdateDeleteRetrieveTask, CreateListTasks

urlpatterns = [
    path('workspaces/<int:workspace>/tasks', CreateListTasks.as_view()),
    path('workspaces/<int:workspace>/tasks/<int:pk>', UpdateDeleteRetrieveTask.as_view()),
]
