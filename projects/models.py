from django.db import models

from django.urls import reverse


# 项目基础信息
class Project(models.Model):
    name = models.CharField(max_length=255, verbose_name="项目名称")
    address = models.CharField(max_length=255, verbose_name="项目地址")
    manager = models.CharField(max_length=255, verbose_name="项目经理")
    active = models.BooleanField(default=True, verbose_name='有效')
    text = models.TextField(blank=True, null=True, verbose_name='项目描述')

    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def get_absolute_url(self):
        return reverse('projects:project_detail', args=[self.id])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created', ]
        verbose_name = '项目'
        verbose_name_plural = '项目'


# 项目财务情况
class ProjectFinanceInitialDetail(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='detail')
    accumulated_revenue = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='累计确认收入', default=0)
    accumulated_cost = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='累计确认成本', default=0)
    capitalized_cost = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='合同履约成本', default=0)
    contract_asset = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='合同资产', default=0)
    contract_liability = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='合同负债', default=0)
    acquisition_cost = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='合同取得成本', default=0)
    accumulated_cash_in = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='累计收合同款', default=0)
    accumulated_cash_out = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='累计付合同款', default=0)
    accounts_receivable_balance = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='应收账款', default=0)
    accounts_payable_balance = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='应付账款', default=0)
    vat = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='销项税金', default=0)
    vat_input = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='进项税金', default=0)

    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    @property
    def profit(self):
        return self.accumulated_revenue - self.accumulated_cost

    @property
    def net_cash_flow(self):
        return self.accumulated_cash_in - self.accumulated_cash_out

    @property
    def net_vat(self):
        return self.vat - self.vat_input

    @property
    def net_cash_flow_tax(self):
        return self.net_cash_flow - self.net_vat

    class Meta:
        ordering = ['-created', ]
        verbose_name = '项目初始财务情况'
        verbose_name_plural = '项目初始财务情况'

    def __str__(self):
        return self.project.name + "初始情况"
