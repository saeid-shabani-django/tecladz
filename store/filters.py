import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Product
        fields = {
            'inventory':['lt','gt','exact'],
            'unit_price':[],
            
            'title':['contains']
        }