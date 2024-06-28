from rest_framework.routers import SimpleRouter

from .views import UserWorkspaceRoleViewSet

router = SimpleRouter()
router.register(r"workspaces/<int:workspace>/users", UserWorkspaceRoleViewSet)

urlpatterns = router.urls
