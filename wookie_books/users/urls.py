from django.urls import path

from .views import RegisterView, LoginView, UserListCreateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user_register'),
    path('login/', LoginView.as_view(), name='user_login'),
    path('list/', UserListCreateView.as_view(), name='list_users'),
]
