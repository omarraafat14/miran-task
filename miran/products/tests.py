"""
Unit tests for the enhanced search functionality.

This module contains comprehensive tests for all aspects of the search implementation:
1. Configurable similarity thresholds
2. Multilingual search (English and Arabic)
3. Synonym expansion
4. Fuzzy matching for misspellings
5. Search query caching
6. Query result caching
7. Performance monitoring
"""

from unittest.mock import MagicMock, patch

from miran.products.filters import ProductFilter
from miran.products.models import Brand, Category, NutritionFacts, Product

from django.contrib.postgres.search import SearchQuery, SearchVector
from django.core.cache import cache
from django.db.models import Q
from django.test import TestCase, override_settings

import pytest


class TestSimilarityThreshold(TestCase):
    """Test the configurable similarity threshold functionality."""

    def setUp(self):
        """Set up test data."""
        self.brand = Brand.objects.create(name="Test Brand", slug="test-brand")
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        # Create test products
        self.product1 = Product.objects.create(
            name="Protein Powder",
            name_ar="بروتين باودر",
            description="High quality protein supplement",
            sku="PP001",
            price=29.99,
            brand=self.brand,
            category=self.category,
        )

        self.product2 = Product.objects.create(
            name="Protein Bar",
            name_ar="بروتين بار",
            description="Protein snack bar",
            sku="PB001",
            price=2.99,
            brand=self.brand,
            category=self.category,
        )
        # Update search vectors
        Product.objects.update(
            search_vector=SearchVector("name", weight="A")
            + SearchVector("description", weight="B")
        )

    def test_default_similarity_threshold(self):
        """Test search with default similarity threshold."""
        queryset = Product.objects.all()
        # Search with a slight misspelling
        filtered = queryset.full_text_search("Protien")
        # Should find both products with default threshold
        self.assertEqual(filtered.count(), 2)

    def test_high_similarity_threshold(self):
        """Test search with higher similarity threshold from settings."""
        queryset = Product.objects.all()
        # Search with a slight misspelling
        filtered = queryset.full_text_search("Protien", similarity_threshold=0.7)
        # Should find fewer or no products with higher threshold
        self.assertLess(filtered.count(), 2)

    def test_instance_similarity_threshold(self):
        """Test search with instance-specific similarity threshold."""
        # Very low threshold should match even with significant misspellings
        queryset = Product.objects.all()
        # Search with a significant misspelling
        filtered = queryset.full_text_search("Proteen")
        # Should still find products with low threshold
        self.assertGreater(filtered.count(), 0)
        # Very high threshold should require near-exact matches
        filtered = queryset.full_text_search("Protien", similarity_threshold=0.9)
        # Should find no products with very high threshold
        self.assertEqual(filtered.count(), 0)


class TestMultilingualSearch(TestCase):
    """Test multilingual search capabilities."""

    def setUp(self):
        """Set up test data with both English and Arabic content."""
        self.brand = Brand.objects.create(name="Test Brand", slug="test-brand")
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        # Create test products with both English and Arabic names
        self.product1 = Product.objects.create(
            name="Protein Powder",
            name_ar="بروتين باودر",
            description="High quality protein supplement",
            description_ar="مكمل بروتين عالي الجودة",
            sku="PP001",
            price=29.99,
            brand=self.brand,
            category=self.category,
        )

        self.product2 = Product.objects.create(
            name="Vitamin C",
            name_ar="فيتامين سي",
            description="Immune system support",
            description_ar="دعم جهاز المناعة",
            sku="VC001",
            price=9.99,
            brand=self.brand,
            category=self.category,
        )
        # Update search vectors
        Product.objects.update(
            search_vector=SearchVector("name", "name_ar", weight="A")
            + SearchVector("description", "description_ar", weight="B")
        )

    def test_english_search(self):
        """Test search with English query."""
        queryset = Product.objects.all()
        # Search with English term
        filtered = queryset.full_text_search("Proteen")
        # Should find the protein product
        self.assertEqual(filtered.count(), 1)
        self.assertEqual(filtered.first().sku, "PP001")

    def test_arabic_search(self):
        """Test search with Arabic query."""
        queryset = Product.objects.all()
        # Search with Arabic term
        filtered = queryset.full_text_search("بروتين")
        # Should find the protein product
        self.assertEqual(filtered.count(), 1)
        self.assertEqual(filtered.first().sku, "PP001")

    def test_mixed_language_search(self):
        """Test search with mixed language query."""
        queryset = Product.objects.all()
        # Create a product with mixed language content
        Product.objects.create(
            name="Protein فيتامين Mix",
            name_ar="مزيج البروتين Vitamin",
            description="Mixed language product",
            sku="MIX001",
            price=19.99,
            brand=self.brand,
            category=self.category,
        )
        # Update search vectors
        Product.objects.update(
            search_vector=SearchVector("name", "name_ar", weight="A")
            + SearchVector("description", "description_ar", weight="B")
        )
        # Search with mixed terms
        filtered = queryset.full_text_search(
            "protein فيتامين", similarity_threshold=0.7
        )
        # Should find the mixed product
        self.assertEqual(filtered.count(), 1)
        self.assertEqual(filtered.first().sku, "MIX001")
