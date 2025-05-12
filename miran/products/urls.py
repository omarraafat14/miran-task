from django.urls import include, path

from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register("path", views.)
urlpatterns = [
    path("", include(router.urls)),
]
