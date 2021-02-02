from django.contrib import admin
from .models import IncomeSettlement, PaymentSettlement


@admin.register(IncomeSettlement)
class IncomeSettlementAdmin(admin.ModelAdmin):
    list_display = ['settle_prepayment',
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
                    ]


@admin.register(PaymentSettlement)
class PaymentSettlementAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'payment_prepaid',
        'payment_normal',
        'payment_other',
        'deduction_prepayment',
        'deduction_warranty',
        'deduction_damage',
        'deduction_other',
        'payment_real_prepaid',
        'payment_real_normal',
        'payment_real_material',
        'payment_real_rent',
        'payment_real_design',
        'payment_real_other',
    ]
