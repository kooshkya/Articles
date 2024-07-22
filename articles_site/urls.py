from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('api/signup/', views.SignupView.as_view(), name='signup_api'),
    path('api/login/', views.LoginView.as_view(), name='login_api'),
    path('api/logout/', views.LogoutView.as_view(), name='logout_api'),
]
