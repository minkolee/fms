from django.shortcuts import render, get_object_or_404, reverse, redirect
from entry.models import Entry
from .forms import VatInvoiceForm
from .models import VatInvoice
from django.contrib import messages


# 按照变动记录列出增票信息
def list_by_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)

    contract = entry.contract

    project = contract.contract_project

    invoices = entry.invoices.all()

    quantity = len(invoices)

    return render(request, 'vat/vat_list_by_entry.html',
                  {'entry': entry, 'invoices': invoices, 'quantity': quantity, 'contract': contract,
                   'project': project})


# 新增增值税发票信息

def add_by_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)

    if request.method == 'GET':
        form = VatInvoiceForm()
        return render(request, 'vat/vat_add.html', {'entry': entry, 'form': form})

    else:
        form = VatInvoiceForm(request.POST)
        if form.is_valid():
            current_object = form.save(commit=False)
            current_object.entry = entry
            # 进项税票自动设置为已提交/收到
            if current_object.vat_type == 2:
                current_object.send = True
            current_object.save()
            messages.success(request, '成功添加增值税发票信息')
            return redirect(reverse('vat:vat_list_by_entry', args=[entry_id, ]))
        else:
            return render(request, 'vat/vat_add.html', {'entry': entry, 'form': form})


# 更改增值税发票提交和取消的状态
def change_send_status(request, vat_id):
    invoice = get_object_or_404(VatInvoice, id=vat_id)
    invoice.send = not invoice.send
    invoice.save()
    return redirect(reverse('vat:vat_list_by_entry', args=[invoice.entry.id, ]))


# 编辑增票信息
def edit_vat(request, vat_id):
    invoice = get_object_or_404(VatInvoice, id=vat_id)
    entry = invoice.entry
    if request.method == 'GET':
        form = VatInvoiceForm(instance=invoice)
        return render(request, 'vat/vat_edit.html', {'entry': entry, 'invoice': invoice, 'form': form})

    else:
        form = VatInvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            current_object = form.save(commit=False)
            current_object.entry = entry
            # 进项税票自动设置为已提交/收到
            if current_object.vat_type == 2:
                current_object.send = True
            current_object.save()
            messages.success(request, '成功修改增值税发票信息')
            return redirect(reverse('vat:vat_list_by_entry', args=[entry.id, ]))
        else:
            return render(request, 'vat/vat_edit.html', {'entry': entry, 'invoice': invoice, 'form': form})


# 删除增票信息
def delete_invoice(request, vat_id):
    invoice = get_object_or_404(VatInvoice, id=vat_id)
    messages.success(request, '成功删除增值税发票信息')
    invoice.delete()
    return redirect(reverse('vat:vat_list_by_entry', args=[invoice.entry.id, ]))


