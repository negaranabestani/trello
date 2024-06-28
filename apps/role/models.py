from django.db import models


class Role(models.Model):
    # fields
    name = models.CharField(max_length=64)

    # fk
    workspace = models.ForeignKey("workspace.Workspace", on_delete=models.CASCADE)

    # m2m
    permissions = models.ManyToManyField("auth.Permission")

    # log
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}: {self.name} | {self.workspace.name}"


class UserWorkspaceRole(models.Model):
    # fk
    user = models.ForeignKey("user.User", on_delete=models.PROTECT)
    role = models.ForeignKey("role.Role", on_delete=models.PROTECT)
    workspace = models.ForeignKey("workspace.Workspace", on_delete=models.PROTECT)

    # log
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
