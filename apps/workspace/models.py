from django.core.validators import MinLengthValidator
from django.db import models


class Workspace(models.Model):
    name = models.CharField(max_length=20, validators=[MinLengthValidator(6)])
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}: {self.name}"
