from django.db import models


class About(models.Model):
    version = models.CharField(max_length=10)
    detail = models.TextField()
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return self.version

    class Meta:
        ordering = ['-created', ]
        verbose_name = '更新记录'
        verbose_name_plural = '更新记录'
