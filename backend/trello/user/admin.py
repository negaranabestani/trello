from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import TrelloUser
from django.contrib.auth.models import Group
from django.contrib import admin


class TrelloUserCreationForm(UserCreationForm):
    class Meta:
        model = TrelloUser
        fields = [
            "email",
            "password",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions"
        ]


class TrelloUserChangeForm(UserChangeForm):
    class Meta:
        model = TrelloUser
        fields = [
            "email",
            "password",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions"
        ]

# @admin.register(TrelloUser)
class TrelloUserAdmin(UserAdmin):
    add_form = TrelloUserCreationForm
    form = TrelloUserChangeForm
    model = TrelloUser
    list_display = (
        "email",
        "created_at",
        "updated_at",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "created_at",
        "updated_at",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": (
            "email",
            "created_at",
            "updated_at",
            "password")}
         ),
        ("Permissions", {"fields": (
            "is_staff",
            "is_active",
            "groups",
            "user_permissions")}
         ),
    )
    add_fieldsets = (
        (None, {"fields": (
            "created_at",
            "updated_at",
            "email",
            "password1",
            "password2",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions")}
         ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(TrelloUser, TrelloUserAdmin)
admin.site.unregister(Group)
