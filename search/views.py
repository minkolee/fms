from django.shortcuts import render, redirect
from projects.models import Project
from contracts.models import Contract
from settlements.models import IncomeSettlement, PaymentSettlement
from entry.models import Entry
from django.db.models import Q


def search_text(request):
    # 搜索字符串
    target_text = request.GET.get('search', None)

    # 如果有搜索字符串，进行正常搜索
    if target_text:
        # 搜索项目名称
        project_result = Project.objects.filter(Q(name__contains=target_text) | Q(text__contains=target_text))
        project_number = project_result.count()

        # 搜索合同名称
        contract_result = Contract.objects.filter(Q(contract_name__contains=target_text)
                                                  | Q(contract_primary__contains=target_text)
                                                  | Q(contract_secondary1__contains=target_text)
                                                  | Q(contract_secondary2__contains=target_text)
                                                  | Q(contract_secondary3__contains=target_text)
                                                  | Q(contract_contact__contains=target_text)
                                                  | Q(contract_detail__contains=target_text)
                                                  )
        contract_number = contract_result.count()

        # 搜索结算名称
        payment_settlement_result = PaymentSettlement.objects.filter(name__contains=target_text)
        payment_settlement_number = payment_settlement_result.count()

        income_settlement_result = IncomeSettlement.objects.filter(name__contains=target_text)
        income_settlement_number = income_settlement_result.count()

        # 搜索明细名称
        entry_result = Entry.objects.filter(description__contains=target_text)
        entry_number = entry_result.count()

        total_number = project_number + contract_number + payment_settlement_number + income_settlement_number + entry_number

        return render(request, 'search/result.html', {
            'project_result': project_result,
            'project_number': project_number,
            'contract_result': contract_result,
            'contract_number': contract_number,
            'payment_settlement_result': payment_settlement_result,
            'payment_settlement_number': payment_settlement_number,
            'income_settlement_result': income_settlement_result,
            'income_settlement_number': income_settlement_number,
            'entry_result': entry_result,
            'entry_number': entry_number,
            'total_number': total_number,
            'is_blank': False,
            'target_text': target_text
        })

    # 返回空白页面
    else:
        return render(request, 'search/result.html', {'is_blank': True})
