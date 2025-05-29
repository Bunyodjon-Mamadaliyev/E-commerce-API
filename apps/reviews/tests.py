from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.reviews.models import Review
from apps.products.models import Product, Category, Attribute
from decimal import Decimal

User = get_user_model()

class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone='998907654321',
            name='Reviewer',
            email='review@example.com',
            password='reviewpass123'
        )
        self.category = Category.objects.create(name='Accessories', slug='accessories')
        self.attribute = Attribute.objects.create(color='Red', size='small', material='Leather')
        self.product = Product.objects.create(
            title='Leather Wallet',
            price=Decimal('25.00'),
            category=self.category,
            attributes=self.attribute
        )

    def test_review_creation(self):
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment='Excellent product!'
        )
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.rating, 5)

    def test_review_str_method(self):
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            comment='Good quality'
        )
        self.assertEqual(str(review), f'Review by {self.user} for {self.product}')
