"""Home page and shared HTML page frame."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.database import query_one


def index(request: HttpRequest) -> HttpResponse:
    """Show the project overview with counts from the JSON files."""
    counts = query_one("dashboard_counts")
    context = {
        "employees_count": counts["employees_count"],
        "requests_count": counts["requests_count"],
    }
    return render(request, "homepage/index.html", context)


def page_not_found(
    request: HttpRequest,
    exception: Exception,
) -> HttpResponse:
    """Return the project's 404 page."""
    return render(
        request,
        "homepage/404.html",
        status=404,
    )
