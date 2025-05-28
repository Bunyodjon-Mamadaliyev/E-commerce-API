from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import OrderList
from .serializers import OrderListSerializer
from apps.cart.models import CartItem
from django.contrib.auth import get_user_model

User = get_user_model()

class OrderListView(generics.ListCreateAPIView):
    queryset = OrderList.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data
        shipping_address = data.get('shipping_address')
        notes = data.get('notes', '')
        user_id = data.get('user_id')

        if not user_id:
            return Response({
                "success": False,
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "User ID is required",
                    "details": {
                        "field": "user_id",
                        "message": "You must provide a user ID"
                    }
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({
                "success": False,
                "error": {
                    "code": "INVALID_USER",
                    "message": f"User with ID {user_id} does not exist"
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        cart_items = CartItem.objects.filter(user=user)
        if not cart_items.exists():
            return Response({
                "success": False,
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "The provided data is invalid",
                    "details": {
                        "field": "cart",
                        "message": "Your cart is empty"
                    }
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        subtotal = sum([item.subtotal for item in cart_items])
        shipping_fee = 5
        total = subtotal + shipping_fee
        order = OrderList.objects.create(
            order_number=f"ORD-{user.id}-{OrderList.objects.count() + 1}",
            shipping_address=shipping_address,
            notes=notes,
            subtotal=subtotal,
            shipping_fee=shipping_fee,
            total=total,
            status='processing'
        )
        order.items.set(cart_items)
        order.save()
        serializer = self.get_serializer(order)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)


class OrderDetailView(generics.RetrieveAPIView):
    queryset = OrderList.objects.all()
    serializer_class = OrderListSerializer
