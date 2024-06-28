from rest_framework.viewsets import ModelViewSet

from .models import User


# Create your views here.
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
