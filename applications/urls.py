from django.urls import path

from . import views


app_name = "applications"
urlpatterns = [
    path("", views.request_list, name="list"),
    path("statistics/", views.statistics, name="statistics"),
    path("new/", views.request_create, name="create"),
    path("<int:request_id>/edit/", views.request_update, name="update"),
    path(
        "<int:request_id>/withdraw/",
        views.request_withdraw,
        name="withdraw",
    ),
    path("<int:request_id>/", views.request_detail, name="detail"),
]
