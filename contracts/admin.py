from django.contrib import admin

from .models import ContractType, Contract

@admin.register(ContractType)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Contract)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['contract_id',
                    'contract_name',
                    'contract_type',
                    'contract_project',
                    'contract_price',
                    'contract_text',
                    'contract_detail',
                    'contract_primary',
                    'contract_secondary1',
                    'contract_secondary2',
                    'contract_secondary3',
                    'contract_date',
                    'contract_end_date',
                    'contract_stamp_type',
                    'contract_contactor',
                    'contract_phone',
                    ]
