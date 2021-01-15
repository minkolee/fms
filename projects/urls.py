from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'projects'

urlpatterns = [
    path('list/', views.project_list, name='project_list'),
    path('add/', views.project_add, name='project_add'),
    path('', views.project_list, name='project_default'),
]