from . import filters, models, serializers
from rest_framework import viewsets


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    lookup_field = "slug"
    search_fields = ["name__search"]


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer
    lookup_field = "slug"
    search_fields = ["name__search"]


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    lookup_field = "sku"
    filterset_class = filters.ProductFilter
    ordering_fields = ["price", "created_at"]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .active()
            .select_related("brand", "category")
            .prefetch_related("nutrition")
        )
