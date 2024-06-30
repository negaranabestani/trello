from rest_framework.routers import SimpleRouter

from task.views import TaskViewSet, SubTaskViewSet, CommentViewSet, NotificationViewSet

router = SimpleRouter()
router.register(r"workspaces/(?P<workspace>\d+)/tasks", TaskViewSet)
router.register(r"tasks/(?P<task>\d+)/subtasks", SubTaskViewSet)
router.register(r"tasks/(?P<task>\d+)/comments", CommentViewSet)
router.register(r"notifications", NotificationViewSet)

urlpatterns = router.urls
