from django.urls import path
from .views import WorkspaceDetailUpdateDelete,WorkspaceCreateList

urlpatterns = [
    path('workspaces', WorkspaceCreateList.as_view()),
    path('workspaces/<int:pk>', WorkspaceDetailUpdateDelete.as_view(), name='retrieve-customer'),
]
