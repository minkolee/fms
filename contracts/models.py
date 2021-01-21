from django.db import models


class ContractType(models.Model):
    id = models.IntegerField(choices=((1, '收入合同'), (2, '成本合同'), (3, '其他合同')), primary_key=True)
    name = models.CharField(max_length=4,verbose_name="类型名称")