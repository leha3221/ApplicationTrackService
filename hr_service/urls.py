"""Root URL configuration."""

from django.contrib import admin
from django.urls import include, path

from .settings import DEBUG_TOOLBAR_AVAILABLE


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("employees/", include("employees_web.urls")),
    path("requests/", include("applications.urls")),
]

if DEBUG_TOOLBAR_AVAILABLE:
    urlpatterns.insert(0, path("__debug__/", include("debug_toolbar.urls")))

handler404 = "homepage.views.page_not_found"
