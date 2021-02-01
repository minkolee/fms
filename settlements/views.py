from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import IncomeSettlement
from contracts.models import Contract
from .forms import IncomeSettlementForm
from django.contrib import messages


# 列出合同对应的全部结算记录
def settlement_list(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    settlements = contract.settlements.all()
    quantity = settlements.count()
    return render(request, 'settlements/settlement_list.html',
                  {'settlements': settlements, 'contract': contract, 'quantity': quantity})


# 添加结算记录
def settlement_add(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    if request.method == "GET":
        form = IncomeSettlementForm()
        return render(request, 'settlements/settlement_add.html', {'contract': contract, 'form': form})

    else:
        form = IncomeSettlementForm(request.POST)
        if form.is_valid():
            current_object = form.save(commit=False)
            current_object.contract = contract
            current_object.save()
            messages.success(request, '成功添加结算记录')
            return redirect(reverse('settlements:settlement_list', args=[contract.id, ]))
        return render(request, 'settlements/settlement_add.html', {'contract': contract, 'form': form})


# 修改记录
def settlement_edit(request, settlement_id):
    settlement = get_object_or_404(IncomeSettlement, id=settlement_id)
    contract = settlement.contract

    if request.method == "GET":
        form = IncomeSettlementForm(instance=settlement)
        return render(request, 'settlements/settlement_edit.html',
                      {'form': form, 'contract': contract, 'settlement': settlement})
    else:
        form = IncomeSettlementForm(request.POST, instance=settlement)
        if form.is_valid():
            current_object = form.save(commit=False)
            current_object.contract = contract
            current_object.save()

            messages.success(request, '成功修改结算记录')
            return redirect(reverse('settlements:settlement_detail', args=[settlement.id, ]))

        else:
            return render(request, 'settlements/settlement_edit.html',
                          {'form': form, 'contract': contract, 'settlement': settlement})


# 结算记录详情
def settlement_detail(request, settlement_id):
    settlement = get_object_or_404(IncomeSettlement, id=settlement_id)
    contract = settlement.contract

    return render(request, 'settlements/settlement_detail.html', {'settlement': settlement, 'contract': contract})


# 删除结算记录
def settlement_delete(request, settlement_id):
    if request.method == "POST":
        settlement = get_object_or_404(IncomeSettlement, id=settlement_id)
        contract_id = settlement.contract.id
        settlement.delete()
        messages.success(request, '成功删除结算记录')
        return redirect(reverse('settlements:settlement_list', args=[contract_id, ]))

    else:
        return redirect(reverse('settlements:settlement_detail', args=[settlement_id, ]))
