from django.urls import include, path

from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register("path", views.)
router.register("categories", views.CategoryViewSet)
router.register("brands", views.BrandViewSet)
router.register("products", views.ProductViewSet)
urlpatterns = [
    path("", include(router.urls)),
]
