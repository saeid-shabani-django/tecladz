from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Product, Category, Cart, CartItem, Order, OrderItem
from django.utils.text import slugify


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
