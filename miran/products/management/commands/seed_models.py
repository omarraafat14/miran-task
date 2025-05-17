import random

from django.core.management.base import BaseCommand

from ...models import Brand, Category, NutritionFacts, Product
from faker import Faker


class Command(BaseCommand):
    help = "Adds quotes to the database"

    def handle(self, *args, **options):
        fake = Faker()
        # Create categories
        categories = [
            "Electronics",
            "Clothing",
            "Books",
            "Home & Kitchen",
            "Sports & Outdoors",
            "Toys & Games",
            "Beauty & Personal Care",
            "Automotive",
        ]
        for category in categories:
            Category.objects.create(name=category, slug=fake.slug())
        # Create brands
        brands = [
            "Brand A",
            "Brand B",
            "Brand C",
            "Brand D",
            "Brand E",
            "Brand F",
            "Brand G",
            "Brand H",
        ]
        for brand in brands:
            Brand.objects.create(name=brand, slug=fake.slug())

        for _ in range(10000):
            product = Product.objects.create(
                brand=Brand.objects.order_by("?").first(),
                category=Category.objects.order_by("?").first(),
                name=fake.name(),
                description=fake.text(),
                sku=fake.unique.bothify(text="???-#####"),  # Ensures uniqueness
                price=fake.random_number(digits=5),
            )
            nutrition_facts = NutritionFacts(
                product=product,
                calories=round(random.uniform(50, 1000), 2),
                fat=round(random.uniform(0, 100), 2),
                carbs=round(random.uniform(0, 300), 2),
                protein=round(random.uniform(0, 100), 2),
                sodium=round(random.uniform(0, 2000), 2),
                sugar=round(random.uniform(0, 100), 2),
            )
            nutrition_facts.save()

        print("Completed!!!")
