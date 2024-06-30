from rest_framework.routers import SimpleRouter

from task.views import TaskViewSet, SubTaskViewSet, CommentViewSet

router = SimpleRouter()
router.register(r"workspaces/(?P<workspace>\d+)/tasks", TaskViewSet)
router.register(r"tasks/(?P<task>\d+)/subtasks", SubTaskViewSet)
router.register(r"tasks/(?P<task>\d+)/comments", CommentViewSet)

urlpatterns = router.urls
