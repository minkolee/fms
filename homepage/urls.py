from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'homepage'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('', views.home, name='homepage'),
]
