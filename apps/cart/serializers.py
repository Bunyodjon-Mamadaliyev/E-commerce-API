from rest_framework import serializers
from apps.products.models import Product
from .models import CartItem


class ProductShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'image']


class CartItemCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Product with this ID does not exist.")
        return value


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductShortSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['product', 'quantity', 'subtotal']
        ref_name = 'CartItemSerializer_Cart'

    def create(self, validated_data):
        product = validated_data["product"]
        quantity = validated_data.get("quantity", 1)
        validated_data["subtotal"] = product.price * quantity
        return super().create(validated_data)