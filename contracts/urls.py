from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'contracts'

# URL设计想法如下
# contract/list/<int:project_id>/ 列出一个项目下所有合同
# contract/add/<int:project_id>/ 为当前项目添加合同
# contract/edit/<int:project_id>/<int:contract_id>/ 修改某个项目的合同
# contract/delete/<int:contract_id>/ 删除合同（非管理员禁止）
#

urlpatterns = [
    path('initialize/', views.initialize_contract_type, name='contract_type_initial'),
]

