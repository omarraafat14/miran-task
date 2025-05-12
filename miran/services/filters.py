from rest_framework import filters


class CustomOrderingFilter(filters.OrderingFilter):
    def get_schema_fields(self, view):
        if hasattr(view, "ordering_fields"):
            ordering_fields = view.ordering_fields
        elif hasattr(view, "ordering"):
            ordering_fields = view.ordering
        else:
            ordering_fields = []

        self.ordering_description = ", ".join(ordering_fields)
        return super().get_schema_fields(view)


class CustomSearchFilter(filters.SearchFilter):
    def get_schema_fields(self, view):
        self.search_description = (
            ", ".join(view.search_fields) if hasattr(view, "search_fields") else None
        )
        return super().get_schema_fields(view)
