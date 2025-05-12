from . import filters, models, serializers
from rest_framework import viewsets


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    lookup_field = "slug"


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer
    lookup_field = "slug"


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Product.objects.active()
    serializer_class = serializers.ProductSerializer
    lookup_field = "sku"
    filterset_fields = ["category__slug", "brand__slug"]
    ordering_fields = ["price", "created_at"]
