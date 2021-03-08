from django.urls import path, include
from . import views

app_name = 'contracts'

# URL设计想法如下

# 查
# contract/list/<int:project_id>/ 列出一个项目下所有合同
# 增
# contract/add/<int:project_id>/ 为当前项目添加合同
# 改
# contract/edit/<int:project_id>/<int:contract_id>/ 修改某个项目的合同
# 删
# contract/delete/<int:contract_id>/ 删除合同（只能在当前合同没有收付款的情况下才允许删除）

urlpatterns = [
    path('initialize/contract/', views.initialize_contract_type, name='contract_type_initial'),
    path('initialize/stamp/', views.initialize_stamp, name='contract_stamp_initial'),
    path('list/<int:project_id>/', views.contract_list, name='contract_list'),
    path('add/<int:project_id>/', views.contract_add, name='contract_add'),
    path('edit/<int:project_id>/<int:contract_id>/', views.contract_edit, name='contract_edit'),
    path('delete/<int:project_id>/<int:contract_id>/', views.contract_delete, name='contract_delete'),
    path('detail/<int:project_id>/<int:contract_id>/', views.contract_detail, name='contract_detail'),
]

