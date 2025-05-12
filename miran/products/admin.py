from django.contrib import admin

from . import models
from ..services.admin import BaseModelAdmin
from unfold.admin import StackedInline


class NutritionFactsInline(StackedInline):
    model = models.NutritionFacts
    can_delete = False
    extra = 0


@admin.register(models.Category)
class CategoryAdmin(BaseModelAdmin):
    pass


@admin.register(models.Brand)
class BrandAdmin(BaseModelAdmin):
    pass


@admin.register(models.Product)
class ProductAdmin(BaseModelAdmin):
    list_display = ["name", "brand", "category", "price", "is_active"]
    list_filter = ["brand", "category", "is_active"]
    search_fields = ["name", "sku"]
    search_help_text = "Search by name or sku"
    inlines = [NutritionFactsInline]
