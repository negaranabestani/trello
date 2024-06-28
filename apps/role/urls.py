from rest_framework.routers import SimpleRouter

from .views import UserWorkspaceRoleViewSet

router = SimpleRouter()
router.register(r"workspaces/(?P<workspace>\d+)/users", UserWorkspaceRoleViewSet)

urlpatterns = router.urls
