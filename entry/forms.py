from django import forms
from .models import Entry


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = (
            # 两个文字描述
            'description',
            'note',
            'revenue',  # 损益-贷方-负债收入
            'cost',  # 损益-借方-成本
            'others_profit_loss',  # 当成资产-其他损益科目
            'cash',  # 资产-货币资金
            'capitalized_cost',  # 资产-合同履约成本
            'contract_asset',  # 资产-合同资产
            'acquisition_cost',  # 资产-合同取得成本
            'accounts_receivable',  # 资产-应收账款
            'accounts_prepaid',  # 资产-预付账款余额
            'vat_input',  # 资产-进项税金
            'others_asset',  # 资产-其他资产
            'contract_liability',  # 负债-合同负债
            'accounts_payable',  # 负债-应付账款
            'vat',  # 负债-销项税金
            'others_liability',  # 负债-其他负债
        )
        widgets = {
            'note': forms.TextInput(attrs={'placeholder': '20YY-MM-0NNN'}),
        }
