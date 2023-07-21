from django.urls import path
from django.conf import settings
from . import views

# URL conf
urlpatterns = [
    path('', views.index),
    path('settings.FRONTEND_SECRET_KEY/register/', views.register_user),
    path('settings.FRONTEND_SECRET_KEY/login/', views.login_user),
]
