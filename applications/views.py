"""Web views for кадровые заявления, backed by the existing JSON files."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.database import query_all, query_one


def request_list(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("q", "").strip()
    if query:
        requests = query_all(
            "request_search",
            (query, query, query),
        )
    else:
        requests = query_all("request_list")

    context = {"requests": requests, "query": query}
    return render(request, "applications/request_list.html", context)


def request_detail(request: HttpRequest, request_id: int) -> HttpResponse:
    item = query_one("request_detail", (request_id,))
    context = {"item": item}
    return render(
        request,
        "applications/request_detail.html",
        context,
        status=404 if item is None else 200,
    )


def statistics(request: HttpRequest) -> HttpResponse:
    """Display grouped SQL reports for requests and employees."""
    threshold = request.GET.get("min_requests", "0")
    try:
        minimum = max(0, int(threshold))
    except ValueError:
        minimum = 0
    context = {
        "categories": query_all("request_counts_by_category"),
        "statuses": query_all("request_counts_by_status"),
        "departments": query_all("employee_counts_by_department"),
        "request_departments": query_all("request_counts_by_department"),
        "busy_departments": query_all(
            "departments_above_request_count",
            (minimum,),
        ),
        "minimum": minimum,
    }
    return render(request, "applications/statistics.html", context)
