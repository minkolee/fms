from django.db import models
from django.urls import reverse
from django.db.models import Sum


# 项目基础信息
class Project(models.Model):
    name = models.CharField(max_length=255, verbose_name="项目名称")
    address = models.CharField(max_length=255, verbose_name="项目地址")
    manager = models.CharField(max_length=255, verbose_name="项目经理")
    active = models.BooleanField(default=True, verbose_name='有效')
    text = models.TextField(blank=True, null=True, verbose_name='项目描述')

    start_time = models.DateTimeField(null=True, verbose_name='启动时间', blank=True)
    complete_time = models.DateTimeField(null=True, verbose_name='竣工时间', blank=True)

    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def get_entry_add_url(self):
        return reverse('entry:entry_add_project') + "?p={}".format(self.id)

    def get_absolute_url(self):
        return reverse('projects:project_detail', args=[self.id, ])

    # 是否有对应预算
    def has_budget(self):
        return self.budget.count() != 0

    # 有预算的情况下的预算总收入
    def total_budget_income(self):
        if self.has_budget():

            return self.budget.all().aggregate(result=Sum('target_revenue'))['result']
        else:
            return 0

    # 有预算情况下的预算总成本
    def total_budget_cost(self):
        if self.has_budget():

            return self.budget.all().aggregate(result=Sum('target_cost'))['result']
        else:
            return 0

    def total_budget_expense(self):
        if self.has_budget():

            return self.budget.all().aggregate(result=Sum('target_expense'))['result']
        else:
            return 0

    def total_budget_gross_profit(self):
        if self.has_budget():

            return self.total_budget_income() - self.total_budget_cost()
        else:
            return 0

    def total_budget_net_profit(self):
        if self.has_budget():

            return self.total_budget_gross_profit() - self.total_budget_expense()
        else:
            return 0

    def gross_profit_ratio(self):
        if self.total_budget_income() == 0:
            return 0
        if self.has_budget():
            return self.total_budget_gross_profit() / self.total_budget_income()
        else:
            return 0

    def net_profit_ratio(self):
        if self.total_budget_income() == 0:
            return 0
        if self.has_budget():
            return self.total_budget_net_profit() / self.total_budget_income()
        else:
            return 0

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created', ]
        verbose_name = '项目'
        verbose_name_plural = '项目'

    # 所有的计算公式

    # 累计确认收入
    def total_revenue(self):
        result = self.project_entries.aggregate(Sum('revenue'))['revenue__sum']
        if result:
            return result + self.detail.accumulated_revenue
        return self.detail.accumulated_revenue

    # 累计确认营业成本
    def total_cost(self):
        result = self.project_entries.aggregate(Sum('cost'))['cost__sum']
        if result:
            return result + self.detail.accumulated_cost
        return self.detail.accumulated_cost

    # 合同履约成本合计
    def total_capitalized_cost(self):
        result = self.project_entries.aggregate(Sum('capitalized_cost'))['capitalized_cost__sum']
        if result:
            return result + self.detail.capitalized_cost
        return self.detail.capitalized_cost

    # 合同资产合计
    def total_contract_asset(self):
        result = self.project_entries.aggregate(Sum('contract_asset'))['contract_asset__sum']
        if result:
            return result + self.detail.contract_asset
        return self.detail.contract_asset

    # 合同负债合计
    def total_contract_liability(self):
        result = self.project_entries.aggregate(Sum('contract_liability'))['contract_liability__sum']
        if result:
            return result + self.detail.contract_liability
        return self.detail.contract_liability

    # 合同取得成本合计
    def total_acquisition_cost(self):
        result = self.project_entries.aggregate(Sum('acquisition_cost'))['acquisition_cost__sum']
        if result:
            return result + self.detail.acquisition_cost
        return self.detail.acquisition_cost

    # 累计现金流收入
    def total_accumulated_cash_in(self):
        result = self.project_entries.filter(cash__gt=0).aggregate(Sum('cash'))['cash__sum']
        if result:
            return result + self.detail.accumulated_cash_in
        return self.detail.accumulated_cash_in

    # 累计现金流支出
    def total_accumulated_cash_out(self):
        result = self.project_entries.filter(cash__lt=0).aggregate(Sum('cash'))['cash__sum']
        if result:
            return -result + self.detail.accumulated_cash_out
        return self.detail.accumulated_cash_out

    # 应收账款余额
    def total_accounts_receivable(self):
        result = self.project_entries.aggregate(Sum('accounts_receivable'))['accounts_receivable__sum']
        if result:
            return result + self.detail.accounts_receivable_balance
        return self.detail.accounts_receivable_balance

    # 应付账款余额
    def total_accounts_payable(self):
        result = self.project_entries.aggregate(Sum('accounts_payable'))['accounts_payable__sum']
        if result:
            return result + self.detail.accounts_payable_balance
        return self.detail.accounts_payable_balance

    # 预付账款余额
    def total_accounts_prepaid(self):
        result = self.project_entries.aggregate(Sum('accounts_prepaid'))['accounts_prepaid__sum']
        if result:
            return result + self.detail.accounts_prepaid_balance
        return self.detail.accounts_prepaid_balance

    # 销项税金累计
    def total_vat(self):
        result = self.project_entries.aggregate(Sum('vat'))['vat__sum']
        if result:
            return result + self.detail.vat
        return self.detail.vat

    # 进项税金累计
    def total_vat_input(self):
        result = self.project_entries.aggregate(Sum('vat_input'))['vat_input__sum']
        if result:
            return result + self.detail.vat_input
        return self.detail.vat_input

    # 以下是根据实际情况计算的结果

    # 净现金流
    def current_net_cash_flow(self):
        return self.total_accumulated_cash_in() - self.total_accumulated_cash_out()

    # 当前利润
    def current_profit(self):
        return self.total_revenue() - self.total_cost()

    # 累计增值税
    def current_net_vat(self):
        return self.total_vat() - self.total_vat_input()

    # 分析内容
    # 非合同总支付，即过滤所有项目对应Entry的合同为null的部分
    def project_paid_with_no_contract(self):
        return self.project_entries.filter(contract=None).aggregate(Sum('cash'))['cash__sum']

    # 合同总支付，即过滤所有项目对应Entry的合同为null的部分
    def project_paid_with_contract(self):
        return self.project_entries.exclude(contract=None).filter(cash__lt=0).aggregate(Sum('cash'))['cash__sum']

    # 该项目所有的不对应合同的履约成本合计
    def none_contract_cost(self):
        result = self.project_entries.filter(contract=None).aggregate(Sum('capitalized_cost'))[
            'capitalized_cost__sum']
        if result:
            return result
        else:
            return 0


class ProjectBudget(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='budget')
    cost_type = models.CharField(max_length=255, verbose_name="名称")
    target_revenue = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='目标收入', default=0)
    target_cost = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='目标成本', default=0)
    target_profit = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='目标利润', default=0)
    target_expense = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='间接费用', default=0)
    description = models.TextField(verbose_name="变更说明", blank=True, null=True)
    change_time = models.DateTimeField(null=True, verbose_name='变更时间', blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return self.cost_type

    def actual_profit(self):
        return self.target_revenue - self.target_cost - self.target_expense

    # 以下是预算分析的内容
    # 该预算对应的合同履约成本
    def actual_cost(self):
        queryset_contract = self.contract_budget.filter(contract_budget__id=self.id)
        result = 0

        if len(queryset_contract) > 0:
            for each in queryset_contract:
                result += each.capitalized_cost()

        return result

    class Meta:
        ordering = ['created', ]
        verbose_name = '项目预算'
        verbose_name_plural = '项目预算'


# 项目财务情况
class ProjectFinanceInitialDetail(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='detail')
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

    def is_useful(self):
        return self.accumulated_revenue + self.accumulated_cost + self.capitalized_cost + self.contract_asset + \
               self.contract_liability + self.acquisition_cost + self.accumulated_cash_in + self.accumulated_cash_out \
               + self.accounts_payable_balance + self.accounts_receivable_balance + self.vat_input + self.vat
