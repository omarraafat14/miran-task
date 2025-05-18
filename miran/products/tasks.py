from django.contrib.postgres.search import SearchVector

from celery import shared_task


@shared_task
def update_product_search_vector(product_id):
    from .models import Product

    try:
        product = Product.objects.get(id=product_id)
        vector = (
            SearchVector("name", weight="A", config="english")
            + SearchVector("name_ar", weight="A", config="arabic")
            + SearchVector("description", weight="B", config="english")
            + SearchVector("description_ar", weight="B", config="arabic")
        )
        product.search_vector = vector
        product.save(update_fields=["search_vector"])
    except Product.DoesNotExist:
        pass
