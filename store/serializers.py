from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Product, Category, Cart, CartItem, Order, OrderItem, Customer
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.db import transaction


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "unit_price",
            "description",
            "category",
            "inventory",
            "pure_price",
        ]

    category = serializers.StringRelatedField(read_only=True)
    pure_price = serializers.SerializerMethodField(read_only=True)

    def get_pure_price(self, product):
        if product.has_discount:
            return round(product.unit_price * product.discount, 5)

    def validate(self, data):

        self.discount = float(data["discount"])
        if self.discount < 0.99:
            raise serializers.ValidationError("discount Must be less than 1")
        else:
            return data

    def create(self, validated_data):
        self.title = validated_data.get("title")
        slug = slugify(self.title)
        new_product = Product.objects.create(slug=slug, **validated_data)
        return new_product


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ["id", "first_name", "last_name", "email"]


class CustomerSerializer(serializers.ModelSerializer):

    user = CustomUserSerializer()

    class Meta:
        model = Customer
        fields = ["id", "user", "birth_date", "phone_number"]
        read_only_fields = ["id", "user"]


class ProductCartItemSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "unit_price"]


class CartItemSerializer(ModelSerializer):
    product = ProductCartItemSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "item_price"]

    item_price = serializers.SerializerMethodField()

    def get_item_price(self, item):
        return item.product.unit_price * item.quantity


class CartSerializer(ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "items", "total_price"]
        read_only_fields = [
            "id",
        ]

    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum(
            [item.product.unit_price * item.quantity for item in cart.items.all()]
        )


class CreateCartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity"]

    def create(self, validated_data):
        quantity = validated_data.get("quantity")
        cart_pk = self.context.get("cart_pk")
        product = validated_data.get("product")
        if CartItem.objects.filter(cart_id=cart_pk, product_id=product.id).exists():
            cart_item = CartItem.objects.get(product_id=product.id, cart_id=cart_pk)
            cart_item.quantity += quantity
            cart_item.save()
            return cart_item
        else:
            return CartItem.objects.create(cart_id=cart_pk, **validated_data)


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]


class ProductOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title"]

class OrderItemSerializer(serializers.ModelSerializer):

    product = ProductOrderItemSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "quantity", "unit_price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    customer = CustomerSerializer()

    class Meta:
        model = Order
        fields = ["id", "customer", "status", "items"]


class OrderCreateSerializer(serializers.Serializer):

    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(id=cart_id).exists():
            raise serializers.ValidationError("the cart id you entered does not exist")
        elif Cart.objects.filter(id=cart_id).count() == 0:
            raise serializers.ValidationError("the cart is empty")
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data["cart_id"]
            user_id = self.context.get("user_id")
            customer = Customer.objects.get(user_id=user_id)
            order = Order.objects.create(customer=customer)
            order.save()
            cart = Cart(id=cart_id)
            items = cart.items.all()
            order_items = list()
            for cart_item in items:
                order_item = OrderItem()
                order_item.product = cart_item.product
                order_item.order = order
                order_item.quantity = cart_item.quantity
                order_item.unit_price = cart_item.product.unit_price
                order_items.append(order_item)
                cart_item.delete()
            Cart.objects.get(id=cart_id).delete()
            OrderItem.objects.bulk_create(order_items)
            return order


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]
