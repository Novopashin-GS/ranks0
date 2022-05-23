from django.contrib import admin
from mainapp.models import Item, Order

admin.site.register(Item)


@admin.register(Order)
class OrderItems(admin.ModelAdmin):
    readonly_fields = ('created_at',)
