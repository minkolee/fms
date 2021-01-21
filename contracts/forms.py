from django import forms
from .models import ContractType


class ContractTypeForm(forms.ModelForm):
    class Meta:
        model = ContractType
        fields = (
            'name',)
