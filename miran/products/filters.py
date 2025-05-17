from django.contrib.postgres.search import SearchQuery, SearchRank, TrigramSimilarity
from django.db.models import F, Q

from .models import Product
from django_filters import rest_framework as filters


class FullTextMultilingualSearchFilter(filters.CharFilter):
    def filter(self, queryset, value):
        if not value:
            return queryset

        search_query = SearchQuery(value, config="english") | SearchQuery(
            value, config="arabic"
        )

        return (
            queryset.annotate(
                rank=SearchRank(F("search_vector"), search_query),
                similarity=TrigramSimilarity("name", value)
                + TrigramSimilarity("name_ar", value),
            )
            .filter(Q(search_vector=search_query) | Q(similarity__gt=0.3))
            .order_by("-rank", "-similarity")
        )


class ProductFilter(filters.FilterSet):
    search = FullTextMultilingualSearchFilter()

    class Meta:
        model = Product
        fields = ["search", "brand", "category"]
