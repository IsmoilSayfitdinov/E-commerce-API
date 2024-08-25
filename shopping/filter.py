import django_filters
from .models import ProductsModel

class ProductFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name='category', lookup_expr='exact')
    subcategory = django_filters.NumberFilter(field_name='subcategory', lookup_expr='exact')

    class Meta:
        model = ProductsModel
        fields = ['category', 'subcategory']
