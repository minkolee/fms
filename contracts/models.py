from django.db import models
from projects.models import Project


class ContractType(models.Model):
    id = models.IntegerField(choices=((1, '收入合同'), (2, '成本合同'), (3, '其他合同'), (4, '非合同')), primary_key=True)
    name = models.CharField(max_length=4, verbose_name="类型名称")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id', ]
        verbose_name = '合同类型'
        verbose_name_plural = '合同类型'


class Contract(models.Model):
    # 合同编号
    contract_id = models.CharField(max_length=255, unique=True, verbose_name='合同编号')
    # 合同名称
    contract_name = models.CharField(max_length=255, verbose_name='合同名称')
    # 合同类型
    contract_type = models.ForeignKey(ContractType, related_name='contract_type', verbose_name='合同类型',
                                      on_delete=models.CASCADE)
    # 合同对应的项目
    contract_project = models.ForeignKey(Project, related_name='contracts', verbose_name='项目名称',
                                         on_delete=models.CASCADE)
    # 合同总价款（含税价）
    contract_price = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='合同含税总价', default=0)
    # 签订日期
    contract_date = models.DateTimeField(null=True, verbose_name='签订日期', blank=True)
    # 结束 日期
    contract_end_date = models.DateTimeField(null=True, verbose_name='结束日期', blank=True)
    # 合同类别（用于印花税）
    contract_stamp_type = models.CharField(max_length=255, verbose_name='合同类型')
    # 合同标的
    contract_detail = models.CharField(max_length=255, verbose_name='合同标的')
    # 主要合同对手
    contract_primary = models.CharField(max_length=255, verbose_name='主要合同对手')
    # 其他合同对手
    contract_secondary1 = models.CharField(max_length=255, verbose_name='其他合同对手1', null=True, blank=True)
    contract_secondary2 = models.CharField(max_length=255, verbose_name='其他合同对手2', null=True, blank=True)
    contract_secondary3 = models.CharField(max_length=255, verbose_name='其他合同对手3', null=True, blank=True)
    # 支付条款
    contract_text = models.TextField(blank=True, null=True, verbose_name='支付条款')
    # 联系人
    contract_contactor = models.CharField(max_length=255,blank=True, null=True, verbose_name='联系人')
    # 联系电话
    contract_phone = models.CharField(max_length=255,blank=True, null=True, verbose_name='联系电话')

    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return self.contract_project.name + '-' + self.contract_name

    class Meta:
        ordering = ['-created', ]
        verbose_name = '合同'
        verbose_name_plural = '合同'
