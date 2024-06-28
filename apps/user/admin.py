from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.auth.models import Group
from django.contrib import admin


class TrelloUserAdmin(UserAdmin):
    model = User
    list_display = ("id", "username", "first_name", "last_name", "email", "created_at", "updated_at")
    search_fields = ("id", "username", "first_name", "last_name", "email")


admin.site.register(User, TrelloUserAdmin)
admin.site.unregister(Group)
