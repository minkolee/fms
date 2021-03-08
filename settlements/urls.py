from django.urls import path
from . import views

app_name = 'settlements'

urlpatterns = [
    path('list/<int:contract_id>/', views.settlement_list, name='settlement_list'),
    path('add_income/<int:contract_id>/', views.settlement_add, name='settlement_add'),
    path('edit_income/<int:settlement_id>/', views.settlement_edit, name='settlement_edit'),
    path('detail_income/<int:settlement_id>/', views.settlement_detail, name='settlement_detail'),
    path('delete_income/<int:settlement_id>/', views.settlement_delete, name='settlement_delete'),

    path('list_payment/<int:contract_id>/', views.settlement_payment_list, name='settlement_payment_list'),
    path('add_payment/<int:contract_id>/', views.settlement_payment_add, name='settlement_payment_add'),
    path('edit_payment/<int:settlement_id>/', views.settlement_payment_edit, name='settlement_payment_edit'),
    path('detail_payment/<int:settlement_id>/', views.settlement_payment_detail, name='settlement_payment_detail'),
    path('delete_payment/<int:settlement_id>/', views.settlement_payment_delete, name='settlement_payment_delete'),
]