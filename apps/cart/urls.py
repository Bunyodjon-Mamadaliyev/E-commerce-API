from django.urls import path
from .views import CartListCreateAPIView, CartItemDeleteView


urlpatterns = [
    path('cart/', CartListCreateAPIView.as_view(), name='cart-list-create'),
    path('cart/<int:product_id>/', CartItemDeleteView.as_view(), name='cart-delete'),
]
