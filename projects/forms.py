from django import forms
from .models import Project, ProjectFinanceInitialDetail


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            'name', 'address', 'manager', 'active', 'text',)
        widgets = {
            'name': forms.TextInput(),
            'address': forms.TextInput(),
            'manager': forms.TextInput(),
            'text': forms.Textarea(),
        }


class ProjectInitialDetailForm(forms.ModelForm):
    class Meta:
        model = ProjectFinanceInitialDetail
        fields = (
            'accumulated_revenue',
            'accumulated_cost',
            'capitalized_cost',
            'contract_asset',
            'contract_liability',
            'acquisition_cost',
            'accumulated_cash_in',
            'accumulated_cash_out',
            'accounts_receivable_balance',
            'accounts_payable_balance',
            'vat',
            'vat_input'
        )
