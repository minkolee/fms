from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'contracts'

urlpatterns = [
    path('list/<int:project_id>/', views.contract_list_by_project, name='contract_list_by_project'),

]

