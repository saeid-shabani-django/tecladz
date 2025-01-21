from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Product, Category
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

    category = CategorySerializer()
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
        
