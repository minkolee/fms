from django.db import models
from contracts.models import Contract
from django.urls import reverse
from django.db.models import Sum


class IncomeSettlement(models.Model):
    name = models.CharField(max_length=255, verbose_name="结算说明")
    # 应结算款部分
    settle_prepayment = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='应收结算款-预付款项', default=0)
    settle_design = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='应收结算款-设计服务', default=0)
    settle_management = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='应收结算款-管理服务', default=0)
    settle_material = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='应收结算款-材料销售', default=0)
    settle_construction = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='应收结算款-工程服务', default=0)

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
        return self.real_receivable() - self.reception()

    # 连接到某个合同的外键
    contract = models.ForeignKey(Contract, related_name='settlements', verbose_name="结算记录-收入",
                                 on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return '结算记录-收入'

    def get_absolute_url(self):
        return reverse('settlements:settlement_detail', args=[self.id, ])

    class Meta:
        ordering = ['created', ]
        verbose_name = '结算记录-收入'
        verbose_name_plural = '结算记录-收入'

    def get_entry_add_url(self):
        return reverse('entry:entry_add_project') + "?p={}&c={}&si={}".format(self.contract.contract_project.id,
                                                                              self.contract.id, self.id)

    # 计算结算对应的Entry的收款
    def cal_total_cash_in(self):

        result = self.income_entries.all().filter(cash__gt=0).aggregate(Sum('cash'))['cash__sum']

        if result:
            return result
        else:
            return 0

    # 计算结算对应的总付款金额
    def cal_total_cash_out(self):

        result = self.income_entries.all().filter(cash__lt=0).aggregate(Sum('cash'))['cash__sum']

        if result:
            return -result
        else:
            return 0

    # 判断累计的收款金额是否等于变动中对应的净现金流
    def is_received(self):
        return (self.reception() - (self.cal_total_cash_in() - self.cal_total_cash_out()) == 0) or (
                self.income_entries.all().count() == 0)


class PaymentSettlement(models.Model):
    name = models.CharField(max_length=255, verbose_name="结算说明")

    # 应支付给供应商的款
    payment_prepaid = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='应付结算款-预付款项', default=0)
    payment_normal = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='应付结算款-合同款', default=0)
    payment_other = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='应付结算款-其他', default=0)

    # 支付合计
    def payment_total(self):
        return self.payment_prepaid + self.payment_normal + self.payment_other

    # 扣款部分
    deduction_prepayment = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='扣款-预付款项', default=0)
    deduction_warranty = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='扣款-质保金', default=0)
    deduction_damage = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='扣款-违约金', default=0)
    deduction_other = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='扣款-其他扣款', default=0)

    # 合计扣款
    def deduction(self):
        return self.deduction_prepayment + self.deduction_warranty + self.deduction_damage + self.deduction_other

    # 实际付款
    payment_real_prepaid = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='实际付款-预付款',
                                               default=0)
    payment_real_normal = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='实际付款-工程款', default=0)
    payment_real_material = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='实际付款-材料款', default=0)
    payment_real_rent = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='实际付款-租赁款', default=0)
    payment_real_design = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='实际付款-设计费', default=0)
    payment_real_other = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='实际付款-其他', default=0)

    # 实际应支付结算款
    def real_payable(self):
        return self.payment_total() - self.deduction()

    # 实际付款合计
    def total_paid(self):
        return self.payment_real_prepaid + self.payment_real_normal + \
               self.payment_real_material + self.payment_real_rent + self.payment_real_design + self.payment_real_other

    # 未付余额
    def not_paid_yet(self):
        return self.real_payable() - self.total_paid()

    # 合同外键
    contract = models.ForeignKey(Contract, related_name='settlements_payment', verbose_name="结算记录-支出",
                                 on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return '结算记录-支付'

    class Meta:
        ordering = ['created', ]
        verbose_name = '结算记录-支付'
        verbose_name_plural = '结算记录-支付'

    def get_absolute_url(self):
        return reverse('settlements:settlement_payment_detail', args=[self.id, ])

    def get_entry_add_url(self):
        return reverse('entry:entry_add_project') + "?p={}&c={}&so={}".format(self.contract.contract_project.id,
                                                                              self.contract.id, self.id)

    # 计算结算对应的Entry的收款
    def cal_total_cash_in(self):

        result = self.payment_entries.all().filter(cash__gt=0).aggregate(Sum('cash'))['cash__sum']

        if result:
            return result
        else:
            return 0

    # 计算结算对应的总付款金额
    def cal_total_cash_out(self):

        result = self.payment_entries.all().filter(cash__lt=0).aggregate(Sum('cash'))['cash__sum']

        if result:
            return -result
        else:
            return 0

    # 判断累计的付款金额是否等于本次实际支付
    def is_paid(self):
        return self.total_paid() - (self.cal_total_cash_out() - self.cal_total_cash_in()) == 0
