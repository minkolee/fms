from django import forms
from .models import ContractType, Contract


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = (
            'contract_id',
            'contract_name',
            'contract_type',
            'contract_primary',
            'contract_price',
            'contract_text',
            'contract_secondary1',
            'contract_secondary2',
            'contract_secondary3',
            'contract_stamp_type',
            'contract_detail',
            'contract_date',
            'contract_end_date',
            'contract_contact',
            'contract_phone',
        )
        widgets = {
            'contract_date': forms.DateInput(format="%Y-%m-%d", attrs={'placeholder': '20YY-MM-DD 可不填写'}),
            'contract_end_date': forms.DateInput(format="%Y-%m-%d", attrs={'placeholder': '20YY-MM-DD 可不填写'}),
            'contract_text': forms.Textarea(attrs={'placeholder': '可不填写'}),
            'contract_contact': forms.TextInput(attrs={'placeholder': '可不填写'}),
            'contract_phone': forms.TextInput(attrs={'placeholder': '可不填写'}),
            'contract_secondary1': forms.TextInput(attrs={'placeholder': '可不填写'}),
            'contract_secondary2': forms.TextInput(attrs={'placeholder': '可不填写'}),
            'contract_secondary3': forms.TextInput(attrs={'placeholder': '可不填写'}),
        }
