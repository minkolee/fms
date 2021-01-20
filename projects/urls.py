from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'projects'

urlpatterns = [
    path('list/', views.project_list, name='project_list'),
    path('edit/<int:project_id>/', views.edit_project, name='project_edit'),
    path('detail/<int:project_id>/', views.project_detail, name='project_detail'),
    path('initial/<int:project_id>/', views.edit_initial, name='project_edit_initial'),
    path('budget/<int:project_id>/', views.budget, name='project_budget'),
    path('add/', views.project_add, name='project_add'),
    path('delete/<int:project_id>/', views.delete_project, name='project_delete'),
    path('', views.project_list, name='project_default'),
]
