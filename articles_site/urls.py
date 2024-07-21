from django.urls import path

from . import views

urlpatterns = [
    path('test/', views.test_view, name='landing'),
    path('signup/', views.signup_view, name='signup'),
    path('api/signup/', views.SignupView.as_view(), name='signup_api'),
]
