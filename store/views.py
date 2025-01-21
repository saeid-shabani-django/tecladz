from rest_framework.viewsets import ModelViewSet
from .serializers import ProductSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .models import Product, Category, OrderItem
from django.shortcuts import get_object_or_404, redirect
from rest_framework import status
from rest_framework.response import Response
from .filters import ProductFilter

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["inventory", "unit_price"]
    search_fields = [
        "title",
    ]
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = Product.objects.select_related("category").all()

    def destroy(self, request, pk):
        product = get_object_or_404(Product.objects.select_related("category"), pk=pk)
        if not OrderItem.objects.filter(product=product.id):
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("this is related to the orderitem, delete it first")


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    