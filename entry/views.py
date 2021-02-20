from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from projects.models import Project
from contracts.models import Contract
from .models import Entry
from settlements.models import IncomeSettlement, PaymentSettlement
from .forms import EntryForm
from django.contrib.auth.decorators import login_required


# 列出一个项目的所有变动
@login_required
def entry_list_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    entries = project.project_entries.all()
    quantity = entries.count()
    return render(request, 'entry/entry_list_project.html',
                  {'project': project, 'entries': entries, 'quantity': quantity})


# 列出一个合同对应的所有变动
@login_required
def entry_list_contract(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    project = contract.contract_project
    entries = contract.contract_entries.all()
    quantity = entries.count()
    return render(request, 'entry/entry_list_contract.html',
                  {'project': project, 'entries': entries, 'quantity': quantity, 'contract': contract})


# 仅仅添加只对应项目的变动
@login_required
def entry_add(request):
    # GET直接返回空白表单，通过URL取参数判断内容。把几个对应的id埋到页面中。
    if request.method == "GET":
        project_id = request.GET.get("p") or 0
        contract_id = request.GET.get('c') or 0
        settlement_income_id = request.GET.get('si') or 0
        settlement_payment_id = request.GET.get('so') or 0
        if not project_id and not contract_id and not settlement_income_id and not settlement_payment_id:
            return redirect(reverse('homepage:dashboard'))

        form = EntryForm()
        project = get_object_or_404(Project, id=project_id)

        if contract_id:
            contract = get_object_or_404(Contract, id=contract_id)
            return render(request, 'entry/entry_add.html',
                          {'project_id': project_id, 'contract_id': contract_id,
                           'settlement_income_id': settlement_income_id,
                           'settlement_payment_id': settlement_payment_id,
                           'form': form, 'contract': contract, 'project': project})

        else:
            return render(request, 'entry/entry_add.html',
                          {'project_id': project_id, 'contract_id': contract_id,
                           'settlement_income_id': settlement_income_id,
                           'settlement_payment_id': settlement_payment_id,
                           'form': form, 'project': project})


    else:
        project_id = int(request.POST.get("project_id"))
        contract_id = int(request.POST.get('contract_id'))
        settlement_income_id = int(request.POST.get('settlement_income_id'))
        settlement_payment_id = int(request.POST.get('settlement_payment_id'))

        # 区分三种情况,设置好变量，用于给Form表单设置结果

        project = get_object_or_404(Project, id=project_id)
        contract = None
        settlement_income = None
        settlement_payment = None

        # 有合同id，说明至少是合同
        # 使用四个变量，根据条件来设置剩下的三个变量
        if contract_id:
            # print('是合同')
            contract = get_object_or_404(Contract, id=contract_id)
            if (not settlement_income_id) and (not settlement_payment_id):
                pass
            else:
                if settlement_income_id and settlement_payment_id:
                    settlement_income = get_object_or_404(IncomeSettlement, id=settlement_income_id)
                    settlement_payment = get_object_or_404(PaymentSettlement, id=settlement_payment_id)
                elif settlement_income_id:
                    settlement_income = get_object_or_404(IncomeSettlement, id=settlement_income_id)
                else:
                    settlement_payment = get_object_or_404(PaymentSettlement, id=settlement_payment_id)

        print('设置完毕，打印出来看看结果：')
        print("project {}".format(project))
        print("contract {}".format(contract))
        print("is {}".format(settlement_income))
        print("out {}".format(settlement_payment))

        form = EntryForm(request.POST)
        if form.is_valid():
            current_entry = form.save(commit=False)
            if not current_entry.is_balanced():
                messages.error(request, '变动记录借贷不平，请检查')
                return render(request, 'entry/entry_add.html',
                              {'project_id': project_id, 'contract_id': contract_id,
                               'settlement_income_id': settlement_income_id,
                               'settlement_payment_id': settlement_payment_id,
                               'form': form, 'project': project})
            else:
                current_entry.project = project
                current_entry.contract = contract
                current_entry.income_settlement = settlement_income
                current_entry.payment_settlement = settlement_payment
                current_entry.save()
                messages.success(request, '成功添加变动记录')

                # 根据是否包含合同，来判断转向合同对应变动还是项目对应变动
                if contract_id != 0:
                    return redirect(reverse('entry:contract_entry_list', args=[contract_id, ]))

                return redirect(reverse('entry:project_entry_list', args=[project_id, ]))

        return render(request, 'entry/entry_add.html',
                      {'project_id': project_id, 'contract_id': contract_id,
                       'settlement_income_id': settlement_income_id,
                       'settlement_payment_id': settlement_payment_id,
                       'form': form, 'project': project})


# 编辑
@login_required
def entry_edit(request, entry_id):
    if request.method == "GET":
        entry = get_object_or_404(Entry, id=entry_id)
        project_id = entry.project.id or 0
        project = get_object_or_404(Project, id=project_id)
        contract_id = 0
        settlement_income_id = 0
        settlement_payment_id = 0

        # 也是用分支设置上各个数字
        if entry.contract:
            contract_id = entry.contract.id

        if entry.income_settlement:
            settlement_income_id = entry.income_settlement.id

        if entry.payment_settlement:
            settlement_payment_id = entry.payment_settlement.id

        form = EntryForm(instance=entry)

        return render(request, 'entry/entry_edit.html',
                      {'project_id': project_id, 'contract_id': contract_id,
                       'settlement_income_id': settlement_income_id,
                       'settlement_payment_id': settlement_payment_id,
                       'form': form, 'project': project, 'entry_id': entry_id, 'entry': entry})

    else:
        entry = get_object_or_404(Entry, id=entry_id)
        form = EntryForm(request.POST, instance=entry)
        project_id = int(request.POST.get("project_id"))
        contract_id = int(request.POST.get('contract_id'))
        settlement_income_id = int(request.POST.get('settlement_income_id'))
        settlement_payment_id = int(request.POST.get('settlement_payment_id'))
        project = get_object_or_404(Project, id=project_id)

        print(settlement_income_id)
        print(settlement_payment_id)

        if form.is_valid():

            contract = None
            settlement_income = None
            settlement_payment = None

            if contract_id:
                contract = get_object_or_404(Contract, id=contract_id)

            if settlement_income_id:
                settlement_income = get_object_or_404(IncomeSettlement, id=settlement_income_id)

            if settlement_payment_id:
                settlement_payment = get_object_or_404(PaymentSettlement, id=settlement_payment_id)

            # 直接设置上四个外键即可，无需再查询
            current_entry = form.save(commit=False)

            if current_entry.is_balanced():
                current_entry.project = project
                current_entry.contract = contract
                current_entry.income_settlement = settlement_income
                current_entry.payment_settlement = settlement_payment
                current_entry.save()
                messages.success(request, '成功修改变动记录')

                if contract_id != 0:
                    return redirect(reverse('entry:contract_entry_list', args=[contract_id, ]))

                return redirect(reverse('entry:project_entry_list', args=[project_id, ]))

            else:
                messages.error(request, '借贷方不平，请检查')

                return render(request, 'entry/entry_edit.html',
                              {'project_id': project_id, 'contract_id': contract_id,
                               'settlement_income_id': settlement_income_id,
                               'settlement_payment_id': settlement_payment_id,
                               'form': form, 'project': project, 'entry_id': entry_id, 'entry': entry})

        return render(request, 'entry/entry_edit.html',
                      {'project_id': project_id, 'contract_id': contract_id,
                       'settlement_income_id': settlement_income_id,
                       'settlement_payment_id': settlement_payment_id,
                       'form': form, 'project': project, 'entry_id': entry_id, 'entry': entry})


@login_required
def entry_delete(request, entry_id):
    if request.method == "POST":
        entry = get_object_or_404(Entry, id=entry_id)
        project_id = entry.project.id
        entry.delete()
        messages.success(request, "成功删除变动记录")
        return redirect(reverse('entry:project_entry_list', args=[project_id, ]))


@login_required
def entry_detail(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)

    return render(request, 'entry/entry_detail.html', {'entry': entry})
