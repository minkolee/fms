from django.urls import path
from . import views

app_name = 'vat'

urlpatterns = [
    # 根据变动来列出该变动对应的增值税发票
    path('list/entry/<int:entry_id>/', views.list_by_entry, name='vat_list_by_entry'),
    path('add/entry/<int:entry_id>/', views.add_by_entry, name='vat_add_by_entry'),
    path('change/vat/<int:vat_id>/', views.change_send_status, name='vat_change_status'),
    path('edit/<int:vat_id>/', views.edit_vat, name='vat_edit'),
    path('delete/<int:vat_id>/', views.delete_invoice, name='vat_delete')

]
