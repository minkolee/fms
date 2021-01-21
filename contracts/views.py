from django.shortcuts import render, get_object_or_404
from projects.models import Project
from django.contrib import messages
from .models import ContractType


# 初始化合同类型的函数，找个链接执行一下即可。考虑将最后一个菜单设置为系统维护。
def initialize_contract_type(request):
    types = ContractType.objects.all()

    names = {1: '收入合同',
             2: '成本合同',
             3: '其他合同',
             4: '非合同'}

    for each_type in types:
        each_type.delete()

    for i in range(1, 5):
        con = ContractType()
        con.id = i
        con.name = names[i]
        con.save()

    messages.success(request, '成功初始化合同类型')

    return render(request, 'homepage/dashboard.html')
