from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'settlements'

urlpatterns = [
    path('list/<int:contract_id>/', views.settlement_list, name='settlement_list'),
    path('add/<int:contract_id>/', views.settlement_add, name='settlement_add'),
    path('edit/<int:settlement_id>/', views.settlement_edit, name='settlement_edit'),
    path('detail/<int:settlement_id>/', views.settlement_detail, name='settlement_detail'),
    path('delete/<int:settlement_id>/', views.settlement_delete, name='settlement_delete'),

]