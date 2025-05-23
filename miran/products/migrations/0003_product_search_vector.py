# Generated by Django 4.2.21 on 2025-05-16 21:50
from django.contrib.postgres.search import SearchVector

import django.contrib.postgres.search
from django.db import migrations


def compute_search_vector(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    vector = (
        SearchVector("name", weight="A", config="english")
        + SearchVector("description", weight="B", config="english")
        + SearchVector("name_ar", weight="A", config="arabic")
        + SearchVector("description_ar", weight="B", config="arabic")
    )
    Product.objects.update(search_vector=vector)


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_brand_name_ar_brand_name_en_category_name_ar_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="search_vector",
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
        migrations.RunPython(
            compute_search_vector, reverse_code=migrations.RunPython.noop
        ),
    ]
