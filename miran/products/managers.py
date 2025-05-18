from django.contrib.postgres.search import SearchQuery, SearchRank, TrigramSimilarity
from django.db import models

from .conf import DEFAULT_SIMILARITY_THRESHOLD


class CategoryQuerySet(models.QuerySet):
    pass


class BrandQuerySet(models.QuerySet):
    pass


class ProductQueryset(models.QuerySet):

    def active(self) -> models.QuerySet:
        """
        Filter to only active products.

        Returns:
            QuerySet of active products
        """
        return self.filter(is_active=True)

    def with_related(self) -> models.QuerySet:
        """
        Optimize query by prefetching related objects.

        Returns:
            QuerySet with prefetched related objects
        """
        return self.select_related("brand", "category").prefetch_related("nutrition")

    def full_text_search(self, query: str) -> models.QuerySet:
        """
        Perform full-text search on products using PostgreSQL's search capabilities.

        Args:
            query: Search query string
            similarity_threshold: Threshold for trigram similarity matches

        Returns:
            QuerySet of matching products, ordered by relevance
        """
        search_query = SearchQuery(query, config="english") | SearchQuery(
            query, config="arabic"
        )
        return (
            self.annotate(
                rank=SearchRank(models.F("search_vector"), search_query),
                similarity=TrigramSimilarity("name", query)
                + TrigramSimilarity("name_ar", query),
            )
            .filter(
                models.Q(search_vector=search_query)
                | models.Q(similarity__gt=DEFAULT_SIMILARITY_THRESHOLD)
            )
            .order_by("-rank", "-similarity")
        )
