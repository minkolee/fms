from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'entry'

urlpatterns = [
    # 列出某个项目所有的变动记录
    path('list/project/<int:project_id>/', views.entry_list_project, name='project_entry_list'),

    # 用于添加属于项目，不属于合同的变动
    # path('add/p/<int:project_id>/', views.settlement_add, name='settlement_add'),
    # 添加属于项目和属于合同，但没有结算的变动
    # path('add/p/<int:project_id>/c/<int:contract_id>', views.settlement_add, name='settlement_add'),
    # 添加属于结算的变动
    # path('add/p/<int:project_id>/c/<int:contract_id>/s/<int:settlement_id>', views.settlement_add, name='settlement_add'),
]
