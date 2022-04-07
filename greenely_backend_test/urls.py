from django.contrib.auth import login, views
from django.urls import path, include
from django.views.generic import TemplateView

from consumption_api.views import get_data, get_limits

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/login/', views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
    path('data/', get_data),
    path('limits/', get_limits),
]
