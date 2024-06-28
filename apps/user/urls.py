from django.urls import path
from .views import TrelloUserCreate, TrelloUserList, TrelloUserDetailUpdateDelete, LoginView

urlpatterns = [
    path('auth/signup', TrelloUserCreate.as_view(), name='create-customer'),
    path('users', TrelloUserList.as_view()),
    path('users/<int:pk>', TrelloUserDetailUpdateDelete.as_view(), name='retrieve-customer'),
    path('auth/login', LoginView.as_view(), name='login')
]
