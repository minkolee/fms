from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('list/', views.project_list, name='project_list'),
    path('edit/<int:project_id>/', views.edit_project, name='project_edit'),
    path('detail/<int:project_id>/', views.project_detail, name='project_detail'),
    path('initial/<int:project_id>/', views.edit_initial, name='project_edit_initial'),
    path('budget/<int:project_id>/', views.budget, name='project_budget'),
    path('budget/<int:project_id>/all/', views.budget_show_all, name='project_budget_show_all'),
    path('budget/add/<int:project_id>/', views.budget_add, name='project_budget_add'),
    path('budget/edit/<int:budget_id>/', views.budget_edit, name='project_budget_edit'),
    path('budget/delete/<int:project_id>/<int:budget_id>/', views.budget_delete, name='project_budget_delete'),
    path('add/', views.project_add, name='project_add'),
    path('delete/<int:project_id>/', views.delete_project, name='project_delete'),
    path('', views.project_list, name='project_default'),
]
