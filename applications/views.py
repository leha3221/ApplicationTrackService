"""Web views for кадровые заявления, backed by the existing JSON files."""

from html import escape
from pathlib import Path

from django.http import HttpRequest, HttpResponse

from employees import Employee
from homepage.views import page
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

    rows = "".join(
        "<tr>"
        f'<td><a href="/requests/{item.id}/">{item.id}</a></td>'
        f"<td>{escape(item.employee.fio)}</td>"
        f"<td>{escape(item.type)}</td>"
        f"<td>{escape(item.status)}</td>"
        f"<td>{escape(item.date)}</td>"
        "</tr>"
        for item in requests
    )
    if not rows:
        rows = '<tr><td colspan="5">Заявления не найдены.</td></tr>'
    content = f"""
    <h1>Кадровые заявления</h1>
    <form class="row g-2 mb-3" method="get">
        <div class="col-auto"><input class="form-control" name="q"
            value="{escape(query, quote=True)}"
            placeholder="ФИО, тип или статус"></div>
        <div class="col-auto">
            <button class="btn btn-primary">Найти</button>
        </div>
    </form>
    <div class="table-responsive"><table class="table table-striped">
        <thead><tr><th>№</th><th>Сотрудник</th><th>Тип</th>
            <th>Статус</th><th>Дата</th></tr></thead>
        <tbody>{rows}</tbody>
    </table></div>"""
    return HttpResponse(page("Заявления", content))


def request_detail(request: HttpRequest, request_id: int) -> HttpResponse:
    item = next(
        (entry for entry in _load_requests() if entry.id == request_id),
        None,
    )
    if item is None:
        content = '<h1 class="text-danger">Заявление не найдено</h1>'
        return HttpResponse(page("Заявление не найдено", content), status=404)

    content = f"""
    <h1>Заявление № {item.id}</h1>
    <dl class="row">
        <dt class="col-sm-3">Сотрудник</dt>
        <dd class="col-sm-9"><a href="/employees/{item.employee.id}/">
            {escape(item.employee.fio)}</a></dd>
        <dt class="col-sm-3">Тип</dt>
        <dd class="col-sm-9">{escape(item.type)}</dd>
        <dt class="col-sm-3">Статус</dt>
        <dd class="col-sm-9">{escape(item.status)}</dd>
        <dt class="col-sm-3">Дата подачи</dt>
        <dd class="col-sm-9">{escape(item.date)}</dd>
    </dl>
    <a class="btn btn-outline-primary" href="/requests/">
        К списку заявлений
    </a>"""
    return HttpResponse(page(f"Заявление № {item.id}", content))
