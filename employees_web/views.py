"""Web views for employees, using the project's JSON storage."""

from html import escape
from pathlib import Path

from django.http import HttpRequest, HttpResponse

from employees import Employee, find_employee_by_id, find_employees
from storage import load_employees
from homepage.views import page


BASE_DIR = Path(__file__).resolve().parent.parent


def employee_list(request: HttpRequest) -> HttpResponse:
    employees: list[Employee] = load_employees(
        BASE_DIR / "data" / "employees.json"
    )
    query = request.GET.get("q", "").strip()
    if query:
        employees = find_employees(employees, query)

    rows = "".join(
        "<tr>"
        f'<td><a href="/employees/{employee.id}/">{employee.id}</a></td>'
        f"<td>{escape(employee.fio)}</td>"
        f"<td>{escape(employee.department)}</td>"
        f"<td>{employee.age}</td>"
        "</tr>"
        for employee in employees
    )
    if not rows:
        rows = '<tr><td colspan="4">Сотрудники не найдены.</td></tr>'
    content = f"""
    <h1>Сотрудники</h1>
    <form class="row g-2 mb-3" method="get">
        <div class="col-auto"><input class="form-control" name="q"
            value="{escape(query, quote=True)}"
            placeholder="ФИО или подразделение"></div>
        <div class="col-auto">
            <button class="btn btn-primary">Найти</button>
        </div>
    </form>
    <div class="table-responsive"><table class="table table-striped">
        <thead><tr><th>ID</th><th>ФИО</th><th>Подразделение</th>
            <th>Возраст</th></tr></thead>
        <tbody>{rows}</tbody>
    </table></div>"""
    return HttpResponse(page("Сотрудники", content))


def employee_detail(request: HttpRequest, employee_id: int) -> HttpResponse:
    employees: list[Employee] = load_employees(
        BASE_DIR / "data" / "employees.json"
    )
    employee = find_employee_by_id(employees, employee_id)
    if employee is None:
        content = '<h1 class="text-danger">Сотрудник не найден</h1>'
        return HttpResponse(page("Сотрудник не найден", content), status=404)

    content = f"""
    <h1>{escape(employee.fio)}</h1>
    <dl class="row">
        <dt class="col-sm-3">ID</dt><dd class="col-sm-9">{employee.id}</dd>
        <dt class="col-sm-3">Подразделение</dt>
        <dd class="col-sm-9">{escape(employee.department)}</dd>
        <dt class="col-sm-3">Возраст</dt>
        <dd class="col-sm-9">{employee.age}</dd>
    </dl>
    <a class="btn btn-outline-primary" href="/employees/">
        К списку сотрудников
    </a>"""
    return HttpResponse(page(employee.fio, content))
