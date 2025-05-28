from django.contrib import admin
from .models import OrderList

@admin.register(OrderList)
class OrderListAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_number', 'status', 'subtotal', 'shipping_fee', 'total', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'tracking_number', 'shipping_address')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('items',)
