from django.contrib import admin
from .models import CartItem

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'subtotal')
    list_filter = ('user',)
    search_fields = ('user__username', 'product__title')
