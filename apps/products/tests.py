from django.test import TestCase
from decimal import Decimal
from apps.products.models import Category, Attribute, Product

class ProductModelsTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics'
        )
        self.attribute = Attribute.objects.create(
            color='Black',
            size='medium',
            material='Plastic'
        )

    def test_category_creation_and_str(self):
        self.assertEqual(self.category.name, 'Electronics')
        self.assertEqual(str(self.category), 'Electronics')

    def test_attribute_creation_and_str(self):
        self.assertEqual(self.attribute.color, 'Black')
        self.assertEqual(self.attribute.size, 'medium')
        self.assertEqual(self.attribute.material, 'Plastic')
        self.assertEqual(str(self.attribute), 'Black / medium / Plastic')

    def test_product_creation_and_str(self):
        product = Product.objects.create(
            title='Wireless Headphones',
            description='High-quality wireless headphones',
            price=Decimal('150.00'),
            category=self.category,
            attributes=self.attribute,
            average_rating=4.5,
            reviews_count=10,
            likes_count=25,
            is_liked=True,
            in_stock=True
        )

        self.assertEqual(product.title, 'Wireless Headphones')
        self.assertEqual(str(product), 'Wireless Headphones')
        self.assertEqual(product.category, self.category)
        self.assertEqual(product.attributes, self.attribute)
        self.assertEqual(product.price, Decimal('150.00'))
        self.assertEqual(product.average_rating, 4.5)
        self.assertEqual(product.reviews_count, 10)
        self.assertEqual(product.likes_count, 25)
        self.assertTrue(product.is_liked)
        self.assertTrue(product.in_stock)
