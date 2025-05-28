from rest_framework import serializers
from .models import OrderList
from apps.cart.models import CartItem
from apps.products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'image']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['product', 'quantity', 'price', 'subtotal']
        ref_name = 'CartItemSerializer_Cart'

    def get_price(self, obj):
        return obj.product.price


class OrderListSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = OrderList
        fields = ['id', 'order_number', 'created_at', 'updated_at', 'status', 'shipping_address',
            'notes', 'items', 'subtotal', 'shipping_fee', 'total', 'tracking_number', 'user_id',
        ]
