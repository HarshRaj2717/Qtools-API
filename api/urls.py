from django.urls import path
from . import views

# URL conf
urlpatterns = [
    path('', views.index),
    path('register/', views.register_user),
    path('login/', views.login_user),
]
