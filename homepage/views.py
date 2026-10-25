"""Home page and shared HTML page frame."""

from html import escape
from pathlib import Path

from django.http import HttpRequest, HttpResponse

from employees import Employee
from requests import Request
from storage import load_employees, load_requests


BASE_DIR = Path(__file__).resolve().parent.parent


def page(title: str, content: str) -> str:
    """Wrap page content in the shared navigation and Bootstrap layout."""
    bootstrap_url = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/"
        "dist/css/bootstrap.min.css"
    )
    return f"""<!doctype html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title>
    <link rel="stylesheet" href="{bootstrap_url}">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">Кадровые заявления</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/employees/">Сотрудники</a>
                <a class="nav-link" href="/requests/">Заявления</a>
            </div>
        </div>
    </nav>
    <main class="container pb-5">{content}</main>
</body>
</html>"""


def index(request: HttpRequest) -> HttpResponse:
    """Show a project overview backed by the existing JSON files."""
    employees: list[Employee] = load_employees(
        BASE_DIR / "data" / "employees.json"
    )
    requests: list[Request] = load_requests(
        BASE_DIR / "data" / "requests.json", employees
    )
    content = f"""
    <h1 class="display-5">Сервис учёта кадровых заявлений</h1>
    <p class="lead">Просмотр сотрудников и поданных заявлений.</p>
    <div class="row g-3 mt-3">
        <div class="col-md-6"><div class="card"><div class="card-body">
            <h2 class="h5">Сотрудники</h2><p>Всего: {len(employees)}</p>
            <a class="btn btn-primary" href="/employees/">Открыть список</a>
        </div></div></div>
        <div class="col-md-6"><div class="card"><div class="card-body">
            <h2 class="h5">Заявления</h2><p>Всего: {len(requests)}</p>
            <a class="btn btn-secondary" href="/requests/">Открыть список</a>
        </div></div></div>
    </div>"""
    return HttpResponse(page("Главная", content))


def page_not_found(
    request: HttpRequest,
    exception: Exception,
) -> HttpResponse:
    """Return the project's 404 page."""
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную страницу.</p>
    <a class="btn btn-primary" href="/">На главную</a>"""
    return HttpResponse(page("Страница не найдена", content), status=404)
