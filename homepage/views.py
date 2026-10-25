"""Home page and shared HTML page frame."""

from pathlib import Path

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from employees import Employee
from requests import Request
from storage import load_employees, load_requests


BASE_DIR = Path(__file__).resolve().parent.parent


def index(request: HttpRequest) -> HttpResponse:
    """Show the project overview with counts from the JSON files."""
    employees: list[Employee] = load_employees(
        BASE_DIR / "data" / "employees.json"
    )
    requests: list[Request] = load_requests(
        BASE_DIR / "data" / "requests.json", employees
    )
    context = {
        "employees_count": len(employees),
        "requests_count": len(requests),
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
