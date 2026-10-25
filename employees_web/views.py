"""Web views for employees, using the project's JSON storage."""

from pathlib import Path

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from employees import Employee, find_employee_by_id, find_employees
from storage import load_employees


BASE_DIR = Path(__file__).resolve().parent.parent


def employee_list(request: HttpRequest) -> HttpResponse:
    employees: list[Employee] = load_employees(
        BASE_DIR / "data" / "employees.json"
    )
    query = request.GET.get("q", "").strip()
    if query:
        employees = find_employees(employees, query)

    context = {"employees": employees, "query": query}
    return render(request, "employees_web/employee_list.html", context)


def employee_detail(request: HttpRequest, employee_id: int) -> HttpResponse:
    employees: list[Employee] = load_employees(
        BASE_DIR / "data" / "employees.json"
    )
    employee = find_employee_by_id(employees, employee_id)
    context = {"employee": employee}
    return render(
        request,
        "employees_web/employee_detail.html",
        context,
        status=404 if employee is None else 200,
    )
