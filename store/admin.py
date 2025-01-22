from django.contrib import admin
from django.db.models import Count, Prefetch
from .models import Product, Category, Cart, CartItem, Customer, Order, OrderItem



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
    fields = ["id", "product", "quantity"]
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "datetime_created"]
    inlines = [CartItemInline]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "first_name",
        "last_name",
        "email",
    ]
    list_per_page = 10
    ordering = [
        "user__last_name",
        "user__first_name",
    ]
    search_fields = [
        "first_name__istartswith",
        "last_name__istartswith",
    ]

    def first_name(self, customer):
        return customer.user.first_name

    def last_name(self, customer):
        return customer.user.last_name

    def email(self, customer):
        return customer.user.email


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ["product", "quantity", "unit_price"]
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "customer",
        "status",
        "datetime_created",
    ]
    list_editable = ["status"]
    list_per_page = 10
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "quantity", "unit_price"]
