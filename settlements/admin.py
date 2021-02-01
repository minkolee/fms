from django.contrib import admin
from .models import IncomeSettlement


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
