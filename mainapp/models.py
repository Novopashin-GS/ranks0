from django.db import models


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def get_total_cost(self):
        items = self.items.select_related()
        return sum(list(map(lambda x: x.price, items)))


class Item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=128, verbose_name='Название')
    description = models.CharField(max_length=128, verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')

    def __str__(self):
        return self.name

    def get_display_price(self):
        return self.price/100

    class Meta:
        verbose_name = 'объект'
        verbose_name_plural = 'объекты'
