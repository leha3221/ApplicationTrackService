"""Web views for employees, using the project's JSON storage."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.database import query_all, query_one


def employee_list(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("q", "").strip()
    if query:
        employees = query_all("employee_search", (query, query))
    else:
        employees = query_all("employee_list")

    context = {"employees": employees, "query": query}
    return render(request, "employees_web/employee_list.html", context)


def employee_detail(request: HttpRequest, employee_id: int) -> HttpResponse:
    employee = query_one("employee_detail", (employee_id,))
    employee_requests = (
        query_all("employee_requests", (employee_id,))
        if employee is not None
        else []
    )
    context = {
        "employee": employee,
        "requests": employee_requests,
    }
    return render(
        request,
        "employees_web/employee_detail.html",
        context,
        status=404 if employee is None else 200,
    )
