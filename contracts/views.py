from django.shortcuts import render, get_object_or_404, reverse, redirect
from projects.models import Project, ProjectBudget
from django.contrib import messages
from .models import ContractType, Contract, Stamp
from .forms import ContractForm
from django.contrib.auth.decorators import login_required


# 初始化合同类型的函数，找个链接执行一下即可。考虑将最后一个菜单设置为系统维护，仅仅只有管理员可见。
@login_required
def initialize_contract_type(request):
    types = ContractType.objects.all()

    if types.count() == 0:

        names = {1: '收入合同',
                 2: '成本合同',
                 3: '其他合同',
                 4: '非合同'}

        for each_type in types:
            each_type.delete()

        for i in range(1, len(names) + 1):
            con = ContractType()
            con.id = i
            con.name = names[i]
            con.save()

        messages.success(request, '成功初始化合同类型')

    return render(request, 'homepage/dashboard.html')


# 初始化印花税与比例
@login_required
def initialize_stamp(request):
    types = Stamp.objects.all()

    if types.count() == 0:

        names = {
            1: ('购销合同', '0.0003'),
            2: ('加工承揽合同', '0.0005'),
            3: ('建设工程勘察设计合同', '0.0005'),
            4: ('建筑安装工程承包合同', '0.0003'),
            5: ('财产租赁合同', '0.001'),
            6: ('货物运输合同', '0.0005'),
            7: ('仓储保管合同', '0.001'),
            8: ('借款合同', '0.00005'),
            9: ('财产保险合同', '0.00003'),
            10: ('技术合同', '0.0003'),
            11: ('产权转移书据', '0.0005'),
            12: ('无需缴纳印花税', '0'),
        }

        for each_type in types:
            each_type.delete()

        for i in range(1, len(names) + 1):
            con = Stamp()
            con.id = i
            con.name = names[i][0]
            con.rate = names[i][1]
            con.save()

        messages.success(request, '成功初始化印花税')

    return render(request, 'homepage/dashboard.html')


# 列出某个项目对应合同
@login_required
def contract_list(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    quantity = project.contracts.count()
    contracts = project.contracts.all()
    return render(request, 'contracts/contract_list.html',
                  {"project": project, 'quantity': quantity, 'contracts': contracts})


# 宽屏版本
@login_required
def contract_list_wide(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    quantity = project.contracts.count()
    contracts = project.contracts.all()
    return render(request, 'contracts/contract_list_fluid.html',
                  {"project": project, 'quantity': quantity, 'contracts': contracts})


# 添加合同
@login_required
def contract_add(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    budgets = project.budget.all()
    if request.method == 'GET':
        form = ContractForm()
        return render(request, 'contracts/contract_add.html', {'project': project, 'form': form, 'budgets': budgets})
    else:
        form = ContractForm(request.POST)
        budget_id = request.POST.get('contract_budget')
        print(budget_id)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.contract_project = project
            budget = get_object_or_404(ProjectBudget, id=budget_id)
            contract.contract_budget = budget
            contract.save()
            messages.success(request, '成功添加合同：' + contract.contract_name)
            return redirect(reverse('contracts:contract_list', args=[project.id, ]))
        else:
            return render(request, 'contracts/contract_add.html',
                          {'project': project, 'form': form, 'budgets': budgets, 'budget_id': budget_id})


# 修改合同
@login_required
def contract_edit(request, project_id, contract_id):
    project = get_object_or_404(Project, id=project_id)
    contract = get_object_or_404(Contract, id=contract_id)
    budgets = project.budget.all()

    if request.method == "GET":
        form = ContractForm(instance=contract)
        budget_id = contract.contract_budget.id
        return render(request, 'contracts/contract_edit.html',
                      {'form': form, 'project': project, 'contract': contract, 'budgets': budgets,
                       'budget_id': budget_id})

    else:
        budget_id = request.POST.get('contract_budget')
        form = ContractForm(request.POST, instance=contract)
        print(budget_id)

        if form.is_valid():
            current_project = form.save(commit=False)
            current_project.contract_project = project
            budget = get_object_or_404(ProjectBudget, id=budget_id)
            contract.contract_budget = budget
            current_project.save()
            messages.success(request, '成功修改合同信息：' + contract.contract_name)
            return redirect(reverse('contracts:contract_detail', args=[project.id, contract.id]))
        else:
            return render(request, 'contracts/contract_edit.html',
                          {'form': form, 'project': project, 'contract': contract, 'budgets': budgets,
                           'budget_id': budget_id})


# 删除合同
@login_required
def contract_delete(request, project_id, contract_id):
    if request.method == 'POST':
        contract = get_object_or_404(Contract, id=contract_id)
        if contract.contract_project.id == int(project_id):
            contract.delete()
            messages.success(request, '成功删除合同：' + contract.contract_name)

    return redirect(reverse('contracts:contract_list', args=[project_id, ]))


# 合同详情
@login_required
def contract_detail(request, project_id, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'contracts/contract_detail.html', {'contract': contract, 'project': project})
