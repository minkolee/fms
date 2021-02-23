from django.db import models
from django.shortcuts import reverse
from projects.models import Project
from django.db.models import Sum


# 合同类型
class ContractType(models.Model):
    id = models.IntegerField(choices=((1, '收入合同'), (2, '成本合同'), (3, '其他合同'), (4, '非合同')), primary_key=True)
    name = models.CharField(max_length=4, verbose_name="类型名称")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id', ]
        verbose_name = '合同类型'
        verbose_name_plural = '合同类型'


# 印花税
class Stamp(models.Model):
    name = models.CharField(max_length=20, verbose_name='印花税类型', unique=True)
    rate = models.DecimalField(max_digits=10, decimal_places=6, verbose_name='印花税税率')

    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created', ]
        verbose_name = '印花税'
        verbose_name_plural = '印花税'


# 合同
class Contract(models.Model):
    # 合同编号
    contract_id = models.CharField(max_length=255, unique=True, verbose_name='合同编号')
    # 合同名称
    contract_name = models.CharField(max_length=255, verbose_name='合同名称')
    # 合同类型 - 修改成即使重新初始化，会将外键设置为null
    contract_type = models.ForeignKey(ContractType, related_name='contract_type', verbose_name='合同类型',
                                      on_delete=models.CASCADE,
                                      # null=True, blank=True
                                      )
    # 合同对应的项目
    contract_project = models.ForeignKey(Project, related_name='contracts', verbose_name='项目名称',
                                         on_delete=models.CASCADE)
    # 合同总价款（含税价）
    contract_price = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='合同含税总价', default=0)
    # 签订日期
    contract_date = models.DateTimeField(null=True, verbose_name='签订日期', blank=True)
    # 结束日期
    contract_end_date = models.DateTimeField(null=True, verbose_name='结束日期', blank=True)
    # 合同类别（用于印花税）- 修改成即使重新初始化，会将外键设置为null
    contract_stamp_type = models.ForeignKey(Stamp, related_name='stamp', verbose_name="合同类别",
                                            on_delete=models.CASCADE,
                                            # null=True, blank=True
                                            )
    # 合同标的
    contract_detail = models.CharField(max_length=255, verbose_name='合同标的')
    # 主要合同对手
    contract_primary = models.CharField(max_length=255, verbose_name='主要合同对手')
    # 其他合同对手
    contract_secondary1 = models.CharField(max_length=255, verbose_name='其他合同对手1', null=True, blank=True)
    contract_secondary2 = models.CharField(max_length=255, verbose_name='其他合同对手2', null=True, blank=True)
    contract_secondary3 = models.CharField(max_length=255, verbose_name='其他合同对手3', null=True, blank=True)
    # 支付条款
    contract_text = models.TextField(blank=True, null=True, verbose_name='关键条款')
    # 联系人
    contract_contact = models.CharField(max_length=255, blank=True, null=True, verbose_name='联系人')
    # 联系电话
    contract_phone = models.CharField(max_length=255, blank=True, null=True, verbose_name='联系电话')

    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return self.contract_project.name + '-' + self.contract_name

    def get_entry_add_url(self):
        return reverse('entry:entry_add_project') + "?p={}&c={}".format(self.contract_project.id, self.id)

    class Meta:
        ordering = ['created', ]
        verbose_name = '合同'
        verbose_name_plural = '合同'

    def get_absolute_url(self):
        return reverse('contracts:contract_detail', args=[self.contract_project.id, self.id, ])

    # 以下为计算合同的所有相关变动影响的数值

    # 计算合同总收款金额
    def cal_total_cash_in(self):

        result = self.contract_entries.all().filter(cash__gt=0).aggregate(Sum('cash'))['cash__sum']

        if result:
            return result
        else:
            return 0

    # 计算合同总付款金额
    def cal_total_cash_out(self):

        result = self.contract_entries.all().filter(cash__lt=0).aggregate(Sum('cash'))['cash__sum']

        if result:
            return -result
        else:
            return 0

    # 计算是否超付
    def is_overpaid(self):
        return self.contract_price < self.cal_total_cash_out()

    # 计算合同资金收支是否出现问题, 成本合同不会考虑资金收支，仅考虑超付
    def is_net_cash_loss(self):
        return (self.cal_total_cash_in() < self.cal_total_cash_out()) & (self.contract_type.id != 2)

    # 计算结算收款总额
    def jiesuan_cal_total_cash_in(self):
        settlements = self.settlements.all()
        cash_sum = 0

        for settlement in settlements:
            cash_sum = cash_sum + settlement.cal_total_cash_in() - settlement.cal_total_cash_out()
        return cash_sum

    # 计算结算付款总额
    def jiesuan_cal_total_cash_out(self):
        settlements = self.settlements_payment.all()
        cash_sum = 0
        for settlement in settlements:
            cash_sum = cash_sum + settlement.cal_total_cash_out() - settlement.cal_total_cash_in()
        return cash_sum

    # 非结算收款合计
    def normal_cal_total_cash_in(self):
        return self.cal_total_cash_in() - self.jiesuan_cal_total_cash_in()

    # 非结算支付合计
    def normal_cal_total_cash_out(self):
        return self.cal_total_cash_out() - self.jiesuan_cal_total_cash_out()
