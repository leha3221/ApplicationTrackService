from django.core.paginator import Paginator
from django.db.models import Avg, Count, F, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.dateparse import parse_date

from employees_web.models import Employee
from .models import Category, Request, Status


def request_list(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("q", "").strip()
    category_code = request.GET.get("category", "").strip()
    status_code = request.GET.get("status", "").strip()
    employee_id = request.GET.get("employee", "").strip()
    selected_date = request.GET.get("date", "").strip()
    exclude_rejected = request.GET.get("exclude_rejected") == "1"
    sort = request.GET.get("sort", "-date")
    error = ""

    requests = Request.objects.select_related("employee", "category", "status")
    if query:
        requests = requests.filter(
            Q(employee__fio__icontains=query)
            | Q(category__name__icontains=query)
            | Q(status__name__icontains=query)
        )
    if category_code:
        requests = requests.filter(category_id=category_code)
    if status_code:
        requests = requests.filter(status_id=status_code)
    if employee_id:
        if employee_id.isdigit():
            requests = requests.filter(employee_id=int(employee_id))
        else:
            error = "Идентификатор сотрудника должен быть целым числом."
    if selected_date:
        request_date = parse_date(selected_date)
        if request_date is None:
            error = "Укажите дату в формате ГГГГ-ММ-ДД."
        else:
            requests = requests.filter(date=request_date)
    if exclude_rejected:
        requests = requests.exclude(status__name__icontains="отклонено")

    sort_fields = {
        "date": "date",
        "-date": "-date",
        "employee": "employee__fio",
        "-employee": "-employee__fio",
        "category": "category__name",
        "-category": "-category__name",
    }
    requests = requests.order_by(sort_fields.get(sort, "-date"), "-pk")
    page_obj = Paginator(requests, 10).get_page(request.GET.get("page"))
    context = {
        "requests": page_obj.object_list,
        "page_obj": page_obj,
        "query": query,
        "category_code": category_code,
        "status_code": status_code,
        "employee_id": employee_id,
        "selected_date": selected_date,
        "exclude_rejected": exclude_rejected,
        "sort": sort if sort in sort_fields else "-date",
        "categories": Category.objects.all(),
        "statuses": Status.objects.all(),
        "error": error,
    }
    return render(request, "applications/request_list.html", context)


def request_detail(request: HttpRequest, request_id: int) -> HttpResponse:
    item = get_object_or_404(
        Request.objects.select_related("employee", "category", "status"),
        pk=request_id,
    )
    return render(request, "applications/request_detail.html", {"item": item})


def statistics(request: HttpRequest) -> HttpResponse:
    """Display grouped reports using Django ORM aggregation."""
    threshold = request.GET.get("min_requests", "0")
    try:
        minimum = max(0, int(threshold))
    except ValueError:
        minimum = 0

    categories = Category.objects.annotate(
        request_count=Count("requests"), type=F("name")
    ).values("code", "type", "request_count").order_by(
        "-request_count", "type"
    )
    statuses = Status.objects.annotate(
        request_count=Count("requests"), status=F("name")
    ).values("code", "status", "request_count").order_by(
        "-request_count", "status"
    )
    departments = Employee.objects.values("department").annotate(
        employee_count=Count("pk"), average_age=Avg("age")
    ).order_by("-employee_count", "department")
    request_departments = Employee.objects.values("department").annotate(
        request_count=Count("requests")
    ).order_by("-request_count", "department")

    context = {
        "categories": categories,
        "statuses": statuses,
        "departments": departments,
        "request_departments": request_departments,
        "busy_departments": request_departments.filter(
            request_count__gt=minimum
        ),
        "minimum": minimum,
    }
    return render(request, "applications/statistics.html", context)
