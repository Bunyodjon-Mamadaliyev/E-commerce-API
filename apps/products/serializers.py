from rest_framework import serializers
from .models import Product, Category, Attribute

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['id', 'color', 'size', 'material']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    attributes = AttributeSerializer()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'images', 'category',
            'attributes', 'average_rating', 'reviews_count', 'likes_count', 'is_liked',
            'in_stock', 'created_at', 'updated_at',
        ]

    def get_images(self, obj):
        return [obj.image.url] if obj.image else []


class ProductLikeSerializer(serializers.Serializer):
    liked = serializers.BooleanField()
    likes_count = serializers.IntegerField()