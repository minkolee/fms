from django import forms
from .models import VatInvoice


class VatInvoiceForm(forms.ModelForm):
    class Meta:
        model = VatInvoice
        fields = (
            'price_without_vat',
            'vat',
            'invoice_number',
            'send',
        )
        widgets = {
        }
