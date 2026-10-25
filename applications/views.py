"""Web views for кадровые заявления, backed by the existing JSON files."""

from pathlib import Path

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from employees import Employee
from requests import Request, find_requests
from storage import load_employees, load_requests


BASE_DIR = Path(__file__).resolve().parent.parent


def _load_requests() -> list[Request]:
    employees: list[Employee] = load_employees(
        BASE_DIR / "data" / "employees.json"
    )
    return load_requests(BASE_DIR / "data" / "requests.json", employees)


def request_list(request: HttpRequest) -> HttpResponse:
    requests = _load_requests()
    query = request.GET.get("q", "").strip()
    if query:
        requests = find_requests(requests, query)

    context = {"requests": requests, "query": query}
    return render(request, "applications/request_list.html", context)


def request_detail(request: HttpRequest, request_id: int) -> HttpResponse:
    item = next(
        (entry for entry in _load_requests() if entry.id == request_id),
        None,
    )
    context = {"item": item}
    return render(
        request,
        "applications/request_detail.html",
        context,
        status=404 if item is None else 200,
    )
