from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models

from . import managers


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    objects = managers.CategoryQuerySet().as_manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    objects = managers.BrandQuerySet().as_manager()

    def __str__(self):
        return self.name


class NutritionFacts(models.Model):
    # relation
    product = models.OneToOneField(
        "Product", on_delete=models.CASCADE, related_name="nutrition"
    )
    # attributes
    calories = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True
    )
    fat = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    carbs = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    protein = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    sodium = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    sugar = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Nutrition Facts"


class Product(models.Model):
    # relations
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    # attributes
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    search_vector = SearchVectorField(null=True)

    objects = managers.ProductQueryset().as_manager()

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            GinIndex(fields=["search_vector"]),
        ]
