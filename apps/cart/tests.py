from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.cart.models import CartItem
from apps.products.models import Product, Category, Attribute
from decimal import Decimal

User = get_user_model()

class CartItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone='998901234567',
            name='Test User',
            email='testuser@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.attribute = Attribute.objects.create(color='Black', size='medium', material='Plastic')
        self.product = Product.objects.create(
            title='Test Product',
            price=Decimal('100.00'),
            category=self.category,
            attributes=self.attribute
        )

    def test_cart_item_creation(self):
        cart_item = CartItem.objects.create(user=self.user, product=self.product, quantity=2, subtotal=200.00)
        self.assertEqual(cart_item.user, self.user)
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(cart_item.subtotal, Decimal('200.00'))

    def test_cart_item_str_method(self):
        cart_item = CartItem.objects.create(user=self.user, product=self.product, quantity=1, subtotal=100.00)
        self.assertEqual(str(cart_item), '1 x Test Product')
