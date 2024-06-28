from rest_framework.routers import SimpleRouter

from task.views import TaskViewSet, SubTaskViewSet

router = SimpleRouter()
router.register(r"workspaces/(?P<workspace>\d+)/tasks", TaskViewSet)
router.register(r"tasks/(?P<task>\d+)/subtasks", SubTaskViewSet)

urlpatterns = router.urls
