from django.db import models
from entry.models import Entry


# 增值税发票
class VatInvoice(models.Model):
    vat_type = models.SmallIntegerField(choices=((1, '销项税票'), (2, '进项税票')), default=1, verbose_name='发票种类')
    price_without_vat = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='不含税额', default=0)
    vat = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='税额', default=0)
    invoice_number = models.CharField(max_length=8, verbose_name="发票号码")
    description = models.CharField(max_length=255, verbose_name='备注', blank=True, null=True)

    # 外键，关联到某个具体变动，可以为空，表示该发票没有对应的结算
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='invoices', blank=True, null=True)

    # 是否已经交付给客户，这个用一个按钮来反映，可以提交也可以不提交
    send = models.BooleanField(default=False, verbose_name='已收到/交付（进项税票默认为收到，无需勾选）')

    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    # 含税价由不含税价和税额自动计算
    @property
    def vat_type_str(self):
        if self.vat_type == 1:
            return '销项税票'
        else:
            return '进项税票'

    @property
    def price_with_vat(self):
        return self.price_without_vat + self.vat

    # 数值形式的代码，用于方便转换
    @property
    def number(self):
        try:
            return int(self.invoice_number)
        except ValueError:
            return 0

    # 检测发票代码是否有误，如果是0，就说明有误
    def is_error(self):
        return self.number == 0

    def __str__(self):
        return '{}|{}'.format(self.invoice_number, self.price_with_vat)

    class Meta:
        ordering = ['created', ]
        verbose_name = '增值税发票'
        verbose_name_plural = '增值税发票'
