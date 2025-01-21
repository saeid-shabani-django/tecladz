from rest_framework.viewsets import ModelViewSet
from .serializers import ProductSerializer, CategorySerializer,CartSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .models import Product, Category, OrderItem, Cart, CartItem
from django.shortcuts import get_object_or_404, redirect
from rest_framework import status
from rest_framework.response import Response
from .filters import ProductFilter
from .permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAdminUser,IsAuthenticated

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
    permission_classes = [IsAdminOrReadOnly]

    def destory(self, request, pk):

        category_detail = get_object_or_404(Category, pk=pk)

        if len(Product.objects.filter(category=category_detail.id)) > 0:

            return Response(
                "You Cannot Remove This Category, Due TO , its dependency to product object"
            )
        else:

            category_detail.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.prefetch_related("items__product").all()
    serializer_class = CartSerializer
    permission_classes = [IsAdminUser]










































