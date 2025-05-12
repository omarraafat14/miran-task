from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from .swagger import CustomOpenAPISchemaGenerator
from .views import health_check
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication


# Admin settings


main_patterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path("api/", include("miran.users.urls")),
    path("rq/", include("django_rq.urls")),
)
# swagger urls and configuration
schema_view = get_schema_view(
    openapi.Info(
        title="miran API",
        default_version="v1",
        description="miran Swagger Documentation",
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
    authentication_classes=(SessionAuthentication,),
    generator_class=CustomOpenAPISchemaGenerator,
    patterns=main_patterns,
)

urlpatterns = main_patterns


urlpatterns += [
    path("health/", health_check, name="health_check"),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("silk/", include("silk.urls", namespace="silk")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
