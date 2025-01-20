from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="category")
    description = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name="title")
    unit_price = models.DecimalField(max_digits=7, decimal_places=3)
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    inventory = models.IntegerField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField()
    has_discount = models.BooleanField(default=False, blank=True, null=True)
    discount = models.FloatField(null=True,blank=True)

    def __str__(self):
        return self.title
