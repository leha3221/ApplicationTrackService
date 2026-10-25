"""Root URL configuration."""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("employees/", include("employees_web.urls")),
    path("requests/", include("applications.urls")),
]

handler404 = "homepage.views.page_not_found"
