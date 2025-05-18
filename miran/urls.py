from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import health_check
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication


# Admin settings

i18n_path = [
    path("i18n/", include("django.conf.urls.i18n")),
]

main_patterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path("api/", include("miran.users.urls")),
    path("api/", include("miran.products.urls")),
    path("rq/", include("django_rq.urls")),
)

urlpatterns = i18n_path + main_patterns


urlpatterns += [
    path("health/", health_check, name="health_check"),
    # Schema endpoint
    path(
        "schema/",
        SpectacularAPIView.as_view(
            authentication_classes=[SessionAuthentication],
            permission_classes=[permissions.IsAuthenticated],
        ),
        name="schema",
    ),
    # Swagger UI
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(
            url_name="schema",
            authentication_classes=[SessionAuthentication],
            permission_classes=[permissions.IsAuthenticated],
        ),
        name="swagger-ui",
    ),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("silk/", include("silk.urls", namespace="silk")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
