from django.contrib import admin
from .models import Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = [
        'description',
        'note',
        'project',
        'contract',
        'income_settlement',
        'payment_settlement',
        'revenue',
        'cost',
        'capitalized_cost',
        'contract_asset',
        'contract_liability',
        'acquisition_cost',
        'accounts_receivable',
        'accounts_payable',
        'accounts_prepaid',
        'vat',
        'vat_input',
        'cash',
    ]
