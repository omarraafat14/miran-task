from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from . import conf, filters, models, serializers
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
        return super().get_queryset().active().with_related()

    @method_decorator(cache_page(conf.SEARCH_QUERY_CACHE_TIMEOUT, cache="default"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(conf.SEARCH_QUERY_CACHE_TIMEOUT, cache="default"))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
