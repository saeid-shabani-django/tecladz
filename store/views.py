from rest_framework.viewsets import ModelViewSet
from .serializers import ProductSerializer, CategorySerializer, CartSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .models import Product, Category, OrderItem, Cart, CartItem, Customer
from django.shortcuts import get_object_or_404, redirect
from rest_framework import status, permissions
from rest_framework.response import Response
from .filters import ProductFilter
from .permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from .permissions import IsAdminOrReadOnly
from .serializers import (
    CreateCartItemSerializer,
    CartItemSerializer,
    UpdateCartItemSerializer,
    CustomUserSerializer,
    CustomerSerializer,
)


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related("category").all()
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["inventory", "unit_price"]
    search_fields = [
        "title",
    ]
    filterset_class = ProductFilter

    def destroy(self, request, pk):
        product = get_object_or_404(Product.objects.select_related("category"), pk=pk)
        if not OrderItem.objects.filter(product=product.id):
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("this is related to the orderitem, delete it first")
   
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.AllowAny()]
        return super().get_permissions()

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


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=["get", "put"], permission_classes=[IsAuthenticated])
    def me(self, request):
        user_id = request.user.id
        customer = Customer.objects.get(id=user_id)

        if request.method == "GET":
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)

        elif request.method == "PUT":
            all_data = request.data
            serializer = CustomerSerializer(customer, data=all_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.prefetch_related("items__product").all()
    serializer_class = CartSerializer
    permission_classes = [IsAdminUser]


class CartItemViewSet(ModelViewSet):
    http_method_names = ["get", "patch", "delete", "head", "options", "post"]

    def get_queryset(self):
        cart_pk = self.kwargs["cart_pk"]
        return CartItem.objects.select_related("product").filter(cart_id=cart_pk).all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        cart_pk = self.kwargs["cart_pk"]
        return {"cart_pk": cart_pk}


class OrderViewSet(ModelViewSet):
    http_method_names = ['post','get','head','options','patch','delete']
    def get_permissions(self):
        if self.request.method in ['DELETE','PATCH']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderCreateSerializer
        if self.request.method == 'PATCH':
            return OrderUpdateSerializer
        return OrderSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return (
                Order.objects.select_related("customer")
                .prefetch_related(
                    Prefetch(
                        "items", queryset=OrderItem.objects.select_related("product")
                    )
                )
                .all()
            )

        return Order.objects.filter(customer__user_id=self.request.user.id)

    def get_serializer_context(self):
        user_id = self.request.user.id
        return {"user_id": user_id}

    def create(self, request, *args, **kwargs):
        created_serializer = OrderCreateSerializer(
            data=request.data, context={"user_id": self.request.user.id}
        )
        created_serializer.is_valid(raise_exception=True)
        final_serializer = created_serializer.save()
        return Response(OrderSerializer(final_serializer).data)
