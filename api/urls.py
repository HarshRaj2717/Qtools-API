from django.urls import path
from django.conf import settings
from . import views

# URL conf
urlpatterns = [
    path('', views.index),
    path(f'{settings.FRONTEND_SECRET_KEY}/', views.index),
    path(f'{settings.FRONTEND_SECRET_KEY}/register/', views.register_user),
    path(f'{settings.FRONTEND_SECRET_KEY}/login/', views.login_user),
    path('<str:user_token>/image-resizer/', views.image_resizer),
]
