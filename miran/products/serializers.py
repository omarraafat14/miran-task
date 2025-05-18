from .models import Brand, Category, NutritionFacts, Product
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "slug"]


class NutritionFactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionFacts
        fields = ["calories", "fat", "carbs", "protein", "sodium", "sugar"]


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    nutrition = NutritionFactsSerializer(read_only=True)
    rank = serializers.ReadOnlyField()
    similarity = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "rank",
            "similarity",
            "description",
            "sku",
            "price",
            "brand",
            "category",
            "nutrition",
        ]
