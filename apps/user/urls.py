from django.urls import path

from .import views

urlpatterns = [
    path('user_register/', views.RegisterView.as_view(), name = 'register_user'),
    path('user_login/', views.LoginView.as_view(), name = 'login-user' )
]