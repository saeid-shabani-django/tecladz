from django.contrib import admin
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "inventory",
        "unit_price",
    ]
    list_per_page = 10
    list_editable = ["unit_price"]
    search_fields = [
        "title",
    ]
    prepopulated_fields = {
        "slug": [
            "title",
        ]
    }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "description",
    ]
    list_per_page = 10

    search_fields = [
        "name",
    ]
