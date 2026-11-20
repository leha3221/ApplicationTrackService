from django.core.paginator import Paginator
from django.db.models import Avg, Count, F, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from employees_web.models import Employee
from .forms import RequestFilterForm, RequestForm
from .models import Category, Request, Status


def request_list(request: HttpRequest) -> HttpResponse:
    filter_form = RequestFilterForm(request.GET or None)
    requests = Request.objects.select_related("employee", "category", "status")
    sort_fields = {
        "date": "date",
        "-date": "-date",
        "employee": "employee__fio",
        "-employee": "-employee__fio",
        "category": "category__name",
        "-category": "-category__name",
    }
    cleaned = filter_form.cleaned_data if filter_form.is_valid() else {}
    query = cleaned.get("q", "")
    category = cleaned.get("category")
    status = cleaned.get("status")
    employee = cleaned.get("employee")
    selected_date = cleaned.get("date")
    exclude_rejected = cleaned.get("exclude_rejected", False)
    sort = cleaned.get("sort") or "-date"

    if query:
        requests = requests.filter(
            Q(employee__fio__icontains=query)
            | Q(category__name__icontains=query)
            | Q(status__name__icontains=query)
        )
    if category:
        requests = requests.filter(category=category)
    if status:
        requests = requests.filter(status=status)
    if employee:
        requests = requests.filter(employee=employee)
    if selected_date:
        requests = requests.filter(date=selected_date)
    if exclude_rejected:
        requests = requests.exclude(status__name__icontains="отклонено")

    requests = requests.order_by(sort_fields.get(sort, "-date"), "-pk")
    page_obj = Paginator(requests, 10).get_page(request.GET.get("page"))
    context = {
        "requests": page_obj.object_list,
        "page_obj": page_obj,
        "filter_form": filter_form,
        "filter_values": request.GET.copy(),
    }
    return render(request, "applications/request_list.html", context)


def request_create(request: HttpRequest) -> HttpResponse:
    form = RequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False)
        if item.employee.age < 18:
            initial_status_code = "5"
        elif item.employee.age > 70:
            initial_status_code = "6"
        else:
            initial_status_code = item.category_id
        initial_status = Status.objects.filter(pk=initial_status_code).first()
        if initial_status is None:
            form.add_error(
                None,
                "Не найден начальный статус заявления. "
                "Проверьте справочник статусов.",
            )
            return render(
                request,
                "applications/request_form.html",
                {
                    "form": form,
                    "page_title": "Новое заявление",
                    "submit_label": "Создать",
                },
            )
        item.status = initial_status
        item.save()
        return redirect("applications:detail", request_id=item.pk)
    return render(
        request,
        "applications/request_form.html",
        {
            "form": form,
            "page_title": "Новое заявление",
            "submit_label": "Создать",
        },
    )


def request_update(request: HttpRequest, request_id: int) -> HttpResponse:
    item = get_object_or_404(Request, pk=request_id)
    if item.status_id == Status.WITHDRAWN_CODE:
        return redirect("applications:detail", request_id=item.pk)
    form = RequestForm(request.POST or None, instance=item)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("applications:detail", request_id=item.pk)
    return render(
        request,
        "applications/request_form.html",
        {
            "form": form,
            "page_title": f"Редактирование заявления № {item.pk}",
            "submit_label": "Сохранить",
            "item": item,
        },
    )


@require_POST
def request_withdraw(request: HttpRequest, request_id: int) -> HttpResponse:
    item = get_object_or_404(Request, pk=request_id)
    withdrawn = get_object_or_404(Status, pk=Status.WITHDRAWN_CODE)
    item.status = withdrawn
    item.save(update_fields=("status",))
    return redirect("applications:detail", request_id=item.pk)


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
        "active_request_count": Request.objects.active().count(),
        "withdrawn_request_count": Request.objects.withdrawn().count(),
        "minimum": minimum,
    }
    return render(request, "applications/statistics.html", context)
