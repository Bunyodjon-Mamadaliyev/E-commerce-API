from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Attribute(models.Model):
    color = models.CharField(max_length=100)
    size = models.SlugField(unique=True)
    material = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.color} / {self.size} / {self.material}"


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products_category', null=True, blank=True)
    attributes = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='products_attributes', null=True, blank=True)
    average_rating = models.FloatField(default=0.0)
    reviews_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    is_liked = models.BooleanField(default=False)
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



