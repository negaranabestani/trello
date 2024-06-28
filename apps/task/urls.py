from rest_framework.routers import SimpleRouter

from task.views import TaskViewSet, SubTaskViewSet

router = SimpleRouter()
router.register(r"workspaces/<int:workspace>/tasks", TaskViewSet)
router.register(r"tasks/<int:task>/subtasks", SubTaskViewSet)

urlpatterns = router.urls
