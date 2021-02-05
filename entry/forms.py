from django import forms
from .models import Entry


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = (
            'description',
            'note',
            # 损益-贷方-负债收入
            'revenue',
            # 损益-借方-成本
            'cost',
            # 资产-合同履约成本
            'capitalized_cost',
            # 资产-合同资产
            'contract_asset',
            # 负债-合同负债
            'contract_liability',
            # 资产-合同取得成本
            'acquisition_cost',

            # 资产-应收账款
            'accounts_receivable',
            # 资产-应付账款
            'accounts_payable',
            # 资产-预付账款余额
            'accounts_prepaid',
            # 负债-销项税金
            'vat',
            # 资产-进项税金
            'vat_input',
            # 资产-货币资金
            'cash',
            # 资产-其他资产
            'others_asset',
            # 负债-其他负债
            'others_liability',
            # 当成资产-其他损益科目
            'others_profit_loss'
        )
        widgets = {

        }
