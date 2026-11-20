from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Employee


def employee_list(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("q", "").strip()
    department = request.GET.get("department", "").strip()
    minimum_age = request.GET.get("min_age", "").strip()
    maximum_age = request.GET.get("max_age", "").strip()
    sort = request.GET.get("sort", "fio")
    error = ""

    employees = Employee.objects.annotate(request_count=Count("requests"))
    if query:
        employees = employees.filter(
            Q(fio__icontains=query) | Q(department__icontains=query)
        )
    if department:
        employees = employees.filter(department__iexact=department)
    for value, field, label in (
        (minimum_age, "age__gte", "минимальный"),
        (maximum_age, "age__lte", "максимальный"),
    ):
        if value:
            try:
                age = int(value)
                if not 1 <= age <= 120:
                    raise ValueError
            except ValueError:
                error = f"Укажите корректный {label} возраст (от 1 до 120)."
            else:
                employees = employees.filter(**{field: age})

    sort_fields = {
        "fio": "fio",
        "-fio": "-fio",
        "age": "age",
        "-age": "-age",
        "department": "department",
        "-department": "-department",
    }
    employees = employees.order_by(sort_fields.get(sort, "fio"), "pk")
    page_obj = Paginator(employees, 10).get_page(request.GET.get("page"))
    context = {
        "employees": page_obj.object_list,
        "page_obj": page_obj,
        "query": query,
        "department": department,
        "min_age": minimum_age,
        "max_age": maximum_age,
        "sort": sort if sort in sort_fields else "fio",
        "error": error,
    }
    return render(request, "employees_web/employee_list.html", context)


def employee_detail(request: HttpRequest, employee_id: int) -> HttpResponse:
    employee = get_object_or_404(
        Employee.objects.prefetch_related(
            "requests__category", "requests__status"
        ),
        pk=employee_id,
    )
    context = {"employee": employee, "requests": employee.requests.all()}
    return render(request, "employees_web/employee_detail.html", context)
