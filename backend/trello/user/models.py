from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TrelloUserManager(BaseUserManager):
    def create_user(
            self,
            email,
            password,
            username,
            created_at,
            updated_at,
            **extra_fields

    ):

        email = self.normalize_email(email)  # lowercase the domain
        user = self.model(
            email=email,
            username=username,
            created_at=created_at,
            updated_at=updated_at,
            **extra_fields
        )
        user.set_password(password)  # hash raw password and set
        user.save()
        return user

    def create_superuser(
            self,
            email,
            password,
            username,
            created_at,
            updated_at,
            **extra_fields
    ):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                _("Superuser must have is_staff=True.")
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                _("Superuser must have is_superuser=True.")
            )
        return self.create_user(
            email=email,
            username=username,
            password=password,
            created_at=created_at,
            updated_at=updated_at,
            **extra_fields
        )


username_validator = RegexValidator(r'^[a-zA-Z0-9_\.]*$',
                                    'Only alphanumeric characters, underscores, and periods are allowed in your username.')


class TrelloUser(AbstractUser):
    username = models.CharField(
        max_length=15, blank=False, null=False, unique=True, validators=[username_validator])
    email = models.EmailField(max_length=255, blank=False, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TrelloUserManager()

    def __str__(self):
        field_values = []
        # for field in self.meta.get_all_field_names():
        #     field_values.append(getattr(self, field, ''))
        # return ' '.join(field_values)
        return "{" + f"{self.get_username()},{self.email},{self.created_at},{self.updated_at}" + "}"
