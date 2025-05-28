from django.urls import path
from .views import CreateReviewView

urlpatterns = [
    path('products/<int:id>/reviews/', CreateReviewView.as_view(), name='create-review'),
]
