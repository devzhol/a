"""
URL configuration for goo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('show-message/', views.show_message, name='show_message'),
    path('show-warning-message/', views.show_warning_message, name='show_warning_message'),
    path('register/', views.register, name='register'),
    path('profiles/', views.ProfileListView.as_view(), name='profile_list'),
    path('cache-demo/', views.cache_demo, name='cache_demo'),
    path('api/sample/', views.sample_api, name='sample_api'),
    path('api/tasks/', views.task_list, name='task_list_api'),
    path('api/tasks/<int:task_id>/', views.task_detail, name='task_detail_api'),
    path('api/users/', views.user_list, name='user_list_api'),
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('send-batch-password-reset/', views.send_batch_password_reset_emails_view, name='send_batch_password_reset'),
    path('admin/', admin.site.urls),
]

