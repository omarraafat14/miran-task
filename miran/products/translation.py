from . import models
from modeltranslation.translator import TranslationOptions, register


@register(models.Brand)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(models.Category)
class BrandTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(models.Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ("name", "description")
