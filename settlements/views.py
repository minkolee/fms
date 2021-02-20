from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import IncomeSettlement, PaymentSettlement
from contracts.models import Contract
from .forms import IncomeSettlementForm, PaymentSettlementForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# 列出合同对应的全部收入结算记录
@login_required
def settlement_list(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    settlements = contract.settlements.all()
    quantity = settlements.count()
    return render(request, 'settlements/settlement_list.html',
                  {'settlements': settlements, 'contract': contract, 'quantity': quantity})


# 列出合同对应的全部支付结算记录
@login_required
def settlement_payment_list(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    settlements = contract.settlements_payment.all()
    quantity = settlements.count()
    return render(request, 'settlements/settlement_payment_list.html',
                  {'settlements': settlements, 'contract': contract, 'quantity': quantity})


# 添加收入结算记录
@login_required
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
            messages.success(request, '成功添加收款结算记录')
            return redirect(reverse('settlements:settlement_list', args=[contract.id, ]))
        return render(request, 'settlements/settlement_add.html', {'contract': contract, 'form': form})


# 付款合同的添加
@login_required
def settlement_payment_add(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    if request.method == "GET":
        form = PaymentSettlementForm()
        return render(request, 'settlements/settlement_payment_add.html', {'contract': contract, 'form': form})

    else:
        form = PaymentSettlementForm(request.POST)
        if form.is_valid():
            current_object = form.save(commit=False)
            current_object.contract = contract
            current_object.save()
            messages.success(request, '成功添加付款结算记录')
            return redirect(reverse('settlements:settlement_payment_list', args=[contract.id, ]))
        return render(request, 'settlements/settlement_payment_add.html', {'contract': contract, 'form': form})


# 编辑修改收入记录
@login_required
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

            messages.success(request, '成功修改收款结算记录')
            return redirect(reverse('settlements:settlement_detail', args=[settlement.id, ]))

        else:
            return render(request, 'settlements/settlement_edit.html',
                          {'form': form, 'contract': contract, 'settlement': settlement})


# 编辑修改支付记录
@login_required
def settlement_payment_edit(request, settlement_id):
    settlement = get_object_or_404(PaymentSettlement, id=settlement_id)
    contract = settlement.contract

    if request.method == "GET":
        form = PaymentSettlementForm(instance=settlement)
        return render(request, 'settlements/settlement_payment_edit.html',
                      {'form': form, 'contract': contract, 'settlement': settlement})
    else:
        form = PaymentSettlementForm(request.POST, instance=settlement)
        if form.is_valid():
            current_object = form.save(commit=False)
            current_object.contract = contract
            current_object.save()

            messages.success(request, '成功修改支付结算记录')
            return redirect(reverse('settlements:settlement_payment_detail', args=[settlement.id, ]))

        else:
            return render(request, 'settlements/settlement_payment_edit.html',
                          {'form': form, 'contract': contract, 'settlement': settlement})


# 收入结算记录详情
@login_required
def settlement_detail(request, settlement_id):
    settlement = get_object_or_404(IncomeSettlement, id=settlement_id)
    contract = settlement.contract

    return render(request, 'settlements/settlement_detail.html', {'settlement': settlement, 'contract': contract})


# 付款结算记录详情
@login_required
def settlement_payment_detail(request, settlement_id):
    settlement = get_object_or_404(PaymentSettlement, id=settlement_id)
    contract = settlement.contract

    return render(request, 'settlements/settlement_payment_detail.html',
                  {'settlement': settlement, 'contract': contract})


# 删除收入结算记录
@login_required
def settlement_delete(request, settlement_id):
    if request.method == "POST":
        settlement = get_object_or_404(IncomeSettlement, id=settlement_id)
        contract_id = settlement.contract.id
        settlement.delete()
        messages.success(request, '成功删除收款结算记录')
        return redirect(reverse('settlements:settlement_list', args=[contract_id, ]))

    else:
        return redirect(reverse('settlements:settlement_detail', args=[settlement_id, ]))


# 删除支付结算记录
@login_required
def settlement_payment_delete(request, settlement_id):
    if request.method == "POST":
        settlement = get_object_or_404(PaymentSettlement, id=settlement_id)
        contract_id = settlement.contract.id
        settlement.delete()
        messages.success(request, '成功删除付款结算记录')
        return redirect(reverse('settlements:settlement_payment_list', args=[contract_id, ]))

    else:
        return redirect(reverse('settlements:settlement_payment_edit', args=[settlement_id, ]))
