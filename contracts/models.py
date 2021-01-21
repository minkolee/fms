from django.db import models


class ContractType(models.Model):
    name = models.IntegerField(verbose_name='合同类型', choices=((0, '收入合同'), (1, '成本合同'), (2, '其他合同')), unique=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='修改时间')
