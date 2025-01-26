from django.db import models
from uuid import uuid4
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="category name")
    description = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name="title")
    unit_price = models.IntegerField()
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )
    inventory = models.IntegerField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True,null=True)
    has_discount = models.BooleanField(default=False, blank=True, null=True)
    discount = models.DecimalField(
        max_digits=2, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return self.title


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=12)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Order(models.Model):
    ORDER_STATUS_PAID = "paid"
    ORDER_STATUS_UNPAID = "unpaid"
    ORDER_STATUS_CANCELED = "caceled"
    ORDER_STATUS = [
        (ORDER_STATUS_PAID, "Paid"),
        (ORDER_STATUS_UNPAID, "Unpaid"),
        (ORDER_STATUS_CANCELED, "Canceled"),
    ]

    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name="orders"
    )
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=1, choices=ORDER_STATUS, default=ORDER_STATUS_UNPAID
    )
    authority_from_zarinpal = models.CharField(max_length=200,blank=True)
    ref_id_from_zarinpal = models.CharField(max_length=200,blank=True)
    data_from_zarinpal = models.TextField(blank=True) # including cart_pan,card_hash etc

    def get_total_price(self):
        items = self.items.all()
        return sum(item.quantity * item.unit_price for item in items)
    
    def __str__(self):
        return f"Order id={self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="order_items"
    )
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.IntegerField()

    class Meta:
        unique_together = [["order", "product"]]


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    datetime_created = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_items"
    )
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    quantity = models.IntegerField()

    class Meta:
        unique_together = [["cart", "product"]]
