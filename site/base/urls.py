from django.contrib.auth import views as auth_views
from django.urls import path

app_name = 'base'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='base/login.html'), name='login'),
]
