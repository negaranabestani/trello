from django.urls import path
from .views import RoleUpdateDelete, CreateRoleOrWorkspaceListUsers

urlpatterns = [
    path('workspaces/<int:workspace>/users', CreateRoleOrWorkspaceListUsers.as_view(), name='create-list-role'),
    path('workspaces/<int:workspace>/users/<int:user>', RoleUpdateDelete.as_view()),
]
