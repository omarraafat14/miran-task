from django.db import models


class CategoryQuerySet(models.QuerySet):
    pass


class BrandQuerySet(models.QuerySet):
    pass


class ProductQueryset(models.QuerySet):

    def active(self):
        return self.filter(is_active=True)
