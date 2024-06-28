from rest_framework.routers import SimpleRouter

from .views import WorkspaceViewSet

router = SimpleRouter()
router.register(r'workspaces', WorkspaceViewSet)

urlpatterns = router.urls
