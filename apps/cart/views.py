from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CartItem
from apps.products.models import Product
from .serializers import CartItemSerializer, CartItemCreateSerializer


class CartListCreateAPIView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CartItemCreateSerializer
        return CartItemSerializer

    def list(self, request, *args, **kwargs):
        cart_items = self.get_queryset()
        serializer = CartItemSerializer(cart_items, many=True)
        total = sum(item.subtotal for item in cart_items)
        items_count = sum(item.quantity for item in cart_items)
        return Response({
            "success": True,
            "data": {
                "items": serializer.data,
                "total": float(total),
                "items_count": items_count
            }
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = Product.objects.get(pk=serializer.validated_data['product_id'])
        quantity = serializer.validated_data['quantity']
        cart_item, created = CartItem.objects.get_or_create(product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.subtotal = cart_item.quantity * product.price
        cart_item.save()
        cart_items = CartItem.objects.all()
        output_serializer = CartItemSerializer(cart_items, many=True)
        total = sum(item.subtotal for item in cart_items)
        items_count = sum(item.quantity for item in cart_items)
        return Response({
            "success": True,
            "data": {
                "items": output_serializer.data,
                "total": float(total),
                "items_count": items_count
            }
        }, status=status.HTTP_200_OK)


class CartItemDeleteView(APIView):
    def delete(self, request, product_id):
        try:
            cart_item = CartItem.objects.get(product_id=product_id)
            cart_item.delete()
        except CartItem.DoesNotExist:
            return Response({
                "success": False,
                "error": {
                    "code": "PRODUCT_NOT_FOUND",
                    "message": "Product not found in cart",
                    "details": {
                        "field": "product_id",
                        "message": f"No cart item found with product ID {product_id}"
                    }
                }
            }, status=status.HTTP_404_NOT_FOUND)
        cart_items = CartItem.objects.all()
        serializer = CartItemSerializer(cart_items, many=True)
        total = sum(item.subtotal for item in cart_items)
        items_count = sum(item.quantity for item in cart_items)
        return Response({
            "success": True,
            "data": {
                "items": serializer.data,
                "total": float(total),
                "items_count": items_count
            }
        }, status=status.HTTP_200_OK)
