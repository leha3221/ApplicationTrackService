from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from applications.models import Request, Status
from employees_web.models import Employee


def index(request: HttpRequest) -> HttpResponse:
    employee_count = Employee.objects.aggregate(total=Count("pk"))["total"]
    request_count = Request.objects.aggregate(total=Count("pk"))["total"]
    status_stats = Status.objects.annotate(request_count=Count("requests"))
    context = {
        "employees_count": employee_count,
        "requests_count": request_count,
        "status_stats": status_stats,
    }
    return render(request, "homepage/index.html", context)


def page_not_found(
    request: HttpRequest,
    exception: Exception,
) -> HttpResponse:
    return render(request, "homepage/404.html", status=404)
