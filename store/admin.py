from django.contrib import admin
from .models import Product, Category, Cart, CartItem


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


class CartItemInline(admin.TabularInline):
    model = CartItem
    fields = ['id','product','quantity']
    extra = 1
   

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=['id','datetime_created']
    inlines = [CartItemInline]



