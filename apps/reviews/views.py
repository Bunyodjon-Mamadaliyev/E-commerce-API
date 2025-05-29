from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.products.models import Product
from .serializers import CreateReviewSerializer, ReviewSerializer


class CreateReviewView(generics.CreateAPIView):
    serializer_class = CreateReviewSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(pk=kwargs['id'])
        except Product.DoesNotExist:
            return Response({
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": "Product not found"
                }
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                product=product,
                user=request.user if request.user.is_authenticated else None
            )
            response_serializer = ReviewSerializer(review)
            return Response({
                "success": True,
                "data": response_serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "error": {
                "code": "INVALID_REQUEST",
                "message": "The provided data is invalid",
                "details": serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)
