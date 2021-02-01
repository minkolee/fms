from django import forms
from .models import IncomeSettlement


class IncomeSettlementForm(forms.ModelForm):
    class Meta:
        model = IncomeSettlement
        fields = (
            'name',
            'settle_prepayment',
            'settle_design',
            'settle_management',
            'settle_material',
            'settle_construction',
            'deduction_prepayment',
            'deduction_warranty',
            'deduction_damage',
            'deduction_other',
            'received_prepayment',
            'received_normal',
            'received_warranty',
            'received_bonus',
            'received_other',
        )
        widgets = {

        }
