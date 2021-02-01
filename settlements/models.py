from django.db import models
from contracts.models import Contract


class IncomeSettlement(models.Model):
    # 应结算款部分
    settle_prepayment = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='应结算款-预付款项', default=0)
    settle_design = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='应结算款-设计服务', default=0)
    settle_management = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='应结算款-管理服务', default=0)
    settle_material = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='应结算款-材料销售', default=0)
    settle_construction = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='应结算款-工程服务', default=0)

    # 合计应结算款项
    def receivable(self):
        return self.settle_prepayment + self.settle_design \
               + self.settle_management + self.settle_material + self.settle_construction

    # 扣款部分
    deduction_prepayment = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='扣款-预收款项', default=0)
    deduction_warranty = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='扣款-质保金', default=0)
    deduction_damage = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='扣款-违约金', default=0)
    deduction_other = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='扣款-其他扣款', default=0)

    # 合计扣款
    def deduction(self):
        return self.deduction_prepayment + self.deduction_warranty + self.deduction_damage + self.deduction_other

    # 实际应收款
    def real_receivable(self):
        return self.receivable() - self.deduction()

    # 实际收款
    received_prepayment = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='实际收款-预收款', default=0)
    received_normal = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='实际收款-进度款', default=0)
    received_warranty = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='实际收款-质保金', default=0)
    received_bonus = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='实际收款-奖励款', default=0)
    received_other = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='实际收款-其他', default=0)

    # 实际收款合计
    def reception(self):
        return self.received_prepayment + self.received_normal + self.received_warranty + self.received_bonus + self.received_other

    # 未收款
    def not_received_yet(self):
        return self.real_receivable()-self.reception()

    # 连接到某个合同的外键
    contract = models.ForeignKey(Contract, related_name='settlements', verbose_name="结算记录", on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return '结算'

    class Meta:
        ordering = ['created', ]
        verbose_name = '结算记录'
        verbose_name_plural = '结算记录'
