from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer, ProductLikeSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['get', 'post'], url_path='like')
    def like(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        if request.method == 'POST':
            product.is_liked = not product.is_liked
            product.likes_count += 1 if product.is_liked else -1
            product.likes_count = max(product.likes_count, 0)
            product.save()

        data = {
            'liked': product.is_liked,
            'likes_count': product.likes_count
        }
        serializer = ProductLikeSerializer(data)
        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)
