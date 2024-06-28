from django.contrib import admin

# Register your models here.
from role.models import Role, UserWorkspaceRole

admin.site.register(Role)
admin.site.register(UserWorkspaceRole)
