from django.db import models
from projects.models import Project
from settlements.models import PaymentSettlement, IncomeSettlement


class Entry(models.Model):
    # 项目外键不能为空
    project = models.ForeignKey(Project, verbose_name='关联项目', related_name='project_entries', on_delete=models.CASCADE)

    # 合同外键可以为空，但项目不能为空，表示无合同付款
    contract = models.ForeignKey(Project, verbose_name='关联合同', related_name='contract_entries',
                                 on_delete=models.CASCADE,
                                 blank=True, null=True)

    # 收款结算，可以为空，表示这一笔变动和收入结算没有关系
    income_settlement = models.ForeignKey(IncomeSettlement, verbose_name='关联收款结算', related_name='income_entries',
                                          on_delete=models.CASCADE, blank=True, null=True)

    # 付款结算，可以为空，表示这一笔变动和收入结算没有关系
    payment_settlement = models.ForeignKey(PaymentSettlement, verbose_name='关联付款结算', related_name='payment_entries',
                                           on_delete=models.CASCADE, blank=True, null=True)

    # 与项目数据保持一致
    accumulated_revenue = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='累计确认收入', default=0)
    accumulated_cost = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='累计确认成本', default=0)
    capitalized_cost = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='合同履约成本', default=0)
    contract_asset = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='合同资产', default=0)
    contract_liability = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='合同负债', default=0)
    acquisition_cost = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='合同取得成本', default=0)
    accumulated_cash_in = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='累计收款', default=0)
    accumulated_cash_out = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='累计付款', default=0)
    accounts_receivable_balance = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='应收账款', default=0)
    accounts_payable_balance = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='应付账款', default=0)
    accounts_prepaid_balance = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='预付分包款', default=0)
    vat = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='销项税金', default=0)
    vat_input = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='进项税金', default=0)

    # 货币资金
    cash = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='货币资金', default=0)

    # 为了借贷平衡而设置的其他资产和负债和损益
    others_asset = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='其他资产', default=0)
    others_liability = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='其他负债', default=0)
    others_profit_loss = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='其他损益', default=0)

    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return self.project.name + "变动记录"

    class Meta:
        ordering = ['created', ]
        verbose_name = '变动记录'
        verbose_name_plural = '变动记录'


