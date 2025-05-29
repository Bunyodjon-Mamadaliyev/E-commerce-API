from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.orders.models import OrderList
from apps.cart.models import CartItem
from apps.products.models import Product, Category, Attribute
from decimal import Decimal

User = get_user_model()

class OrderListModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone='998909999999',
            name='Order User',
            email='orderuser@example.com',
            password='testpass456'
        )
        self.category = Category.objects.create(name='Books', slug='books')
        self.attribute = Attribute.objects.create(color='Blue', size='large', material='Paper')
        self.product = Product.objects.create(
            title='Test Book',
            price=Decimal('50.00'),
            category=self.category,
            attributes=self.attribute
        )
        self.cart_item = CartItem.objects.create(user=self.user, product=self.product, quantity=2, subtotal=100.00)

    def test_order_list_creation(self):
        order = OrderList.objects.create(
            order_number='ORD123456',
            status='pending',
            shipping_address='123 Test St, Tashkent',
            subtotal=100.00,
            shipping_fee=10.00,
            total=110.00
        )
        order.items.add(self.cart_item)
        self.assertEqual(order.order_number, 'ORD123456')
        self.assertEqual(order.total, Decimal('110.00'))
        self.assertEqual(order.items.count(), 1)

    def test_order_list_str_method(self):
        order = OrderList.objects.create(
            order_number='ORD999999',
            status='shipped',
            shipping_address='456 Another St, Tashkent',
            subtotal=80.00,
            shipping_fee=5.00,
            total=85.00
        )
        self.assertEqual(str(order), 'ORD999999')
