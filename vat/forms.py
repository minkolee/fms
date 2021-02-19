from django import forms
from .models import VatInvoice


class VatInvoiceForm(forms.ModelForm):
    class Meta:
        model = VatInvoice
        fields = (
            'vat_type',
            'invoice_number',
            'price_without_vat',
            'vat',
            'send',
        )
        widgets = {

        }
