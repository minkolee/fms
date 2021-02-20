from django.contrib import admin
from .models import VatInvoice


@admin.register(VatInvoice)
class VatInvoiceAdmin(admin.ModelAdmin):
    list_display = [
        'invoice_number',
        'price_without_vat',
        'vat',
        'entry',
        'send',
        'description'
    ]
