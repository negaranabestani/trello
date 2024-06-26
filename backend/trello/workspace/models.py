from django.db import models


class Workspace(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)
    description = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{" + f"{self.name},{self.description},{self.created_at},{self.updated_at}" + "}"
