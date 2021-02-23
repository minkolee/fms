from django import forms
from .models import Project, ProjectFinanceInitialDetail, ProjectBudget


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            'name', 'address', 'manager', 'start_time', 'complete_time', 'active', 'text',)
        widgets = {
            'name': forms.TextInput(),
            'address': forms.TextInput(),
            'start_time': forms.DateInput(format="%Y-%m-%d", attrs={'placeholder': '20YY-MM-DD'}),
            'complete_time': forms.DateInput(format="%Y-%m-%d", attrs={'placeholder': '20YY-MM-DD 未竣工可不填写'}),
            'manager': forms.TextInput(),
            'text': forms.Textarea(attrs={'placeholder': '项目关键信息'}),
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
            'accounts_prepaid_balance',
            'vat',
            'vat_input'
        )


class ProjectBudgetForm(forms.ModelForm):
    class Meta:
        model = ProjectBudget
        fields = (
            'cost_type',
            'target_revenue',
            'target_cost',
            # 'target_profit',
            'target_expense',
            'change_time',
            'description',
        )
        widgets = {
            'change_time': forms.DateInput(format="%Y-%m-%d", attrs={'placeholder': '20YY-MM-DD'}),
        }
