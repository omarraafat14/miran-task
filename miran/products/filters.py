from .models import Product
from django_filters import rest_framework as filters


class ProductFilter(filters.FilterSet):
    search = filters.CharFilter(
        method="filter_by_search",
        help_text="Search products by name, description, or brand in English or Arabic.",
    )
    price_min = filters.NumberFilter(
        field_name="price", lookup_expr="gte", help_text="Minimum price filter"
    )
    price_max = filters.NumberFilter(
        field_name="price", lookup_expr="lte", help_text="Maximum price filter"
    )

    def filter_by_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.full_text_search(value)

    class Meta:
        model = Product
        fields = ["search", "brand", "category", "price_min", "price_max"]
