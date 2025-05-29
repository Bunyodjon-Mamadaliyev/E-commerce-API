from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.users.models import Address

User = get_user_model()

class AddressModelTest(TestCase):
    def test_address_creation_and_str(self):
        address = Address.objects.create(
            street='123 Main St',
            city='Tashkent',
            state='Tashkent',
            postal_code='100100',
            country='Uzbekistan'
        )
        self.assertEqual(str(address), '123 Main St, Tashkent, Uzbekistan')
        self.assertEqual(address.city, 'Tashkent')
        self.assertEqual(address.country, 'Uzbekistan')


class UserModelTest(TestCase):
    def setUp(self):
        self.address = Address.objects.create(
            street='456 Elm St',
            city='Samarkand',
            postal_code='200200',
            country='Uzbekistan'
        )

    def test_create_user(self):
        user = User.objects.create_user(
            phone='998901234567',
            name='Test User',
            email='test@example.com',
            password='securepass123',
            default_shipping_address=self.address
        )
        self.assertEqual(user.phone, '998901234567')
        self.assertEqual(user.name, 'Test User')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('securepass123'))
        self.assertEqual(user.default_shipping_address, self.address)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            phone='998909876543',
            name='Admin User',
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertEqual(superuser.phone, '998909876543')
        self.assertEqual(superuser.name, 'Admin User')
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_user_str_method(self):
        user = User.objects.create_user(
            phone='998901112233',
            name='Ali Valiyev',
            email='ali@example.com',
            password='somepass'
        )
        self.assertEqual(str(user), 'Ali Valiyev')
