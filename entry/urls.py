from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'entry'

urlpatterns = [
    # 列出某个项目所有的变动记录
    path('list/project/<int:project_id>/', views.entry_list_project, name='project_entry_list'),
    path('list/contract/<int:contract_id>/', views.entry_list_contract, name='contract_entry_list'),

    # 用于添加属于项目，不属于合同的变动
    path('add/', views.entry_add, name='entry_add_project'),
    # 编辑变动
    path('edit/<int:entry_id>/', views.entry_edit, name='entry_edit'),

    # 删除
    path('delete/<int:entry_id>/', views.entry_delete, name='entry_delete'),

    # 详情页面

    path('detail/<int:entry_id>/', views.entry_detail, name='entry_detail'),

]
