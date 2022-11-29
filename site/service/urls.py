from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index),
    path('login/', auth_views.LoginView.as_view(template_name='service/login.html'), name='login'),
]
