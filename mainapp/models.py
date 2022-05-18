from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')
    description = models.CharField(max_length=128, verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'объект'
        verbose_name_plural = 'объекты'
