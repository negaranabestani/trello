from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserViewSet, UserRegistration

router = SimpleRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    *router.urls,
    path(r'auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(r'auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(r'auth/signup/', UserRegistration.as_view())
]
