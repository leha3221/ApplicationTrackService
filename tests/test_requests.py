from employees import Employee
from requests import (
    Request,
    cancel_request,
    create_request,
    get_request_statistics,
)


def test_resolve_type_and_status():
    request_type, status = Request.resolve_type_and_status("1", 25)

    assert request_type == "Отпуск"
    assert status == "На согласовании у руководителя"


def test_minor_employee():
    _, status = Request.resolve_type_and_status("1", 17)

    assert status == "Отклонено: сотрудник младше 18 лет"


def test_request_str():
    employee = Employee(1, "Иванов Иван", "IT", 25)
    request = Request(
        1,
        employee,
        "Отпуск",
        "На согласовании у руководителя",
        "2026-09-15",
    )

    assert str(request) == (
        "№ 1 | ФИО: Иванов Иван | Тип: Отпуск | "
        "Дата: 2026-09-15 | Статус: На согласовании у руководителя"
    )


def test_create_request():
    employees = [Employee(1, "Иванов Иван", "IT", 25)]
    requests = []

    request = create_request(requests, employees, 1, "1")

    assert request.id == 1
    assert request.employee is employees[0]
    assert len(requests) == 1


def test_create_request_unknown_employee():
    employees = [Employee(1, "Иванов Иван", "IT", 25)]
    requests = []

    try:
        create_request(requests, employees, 999, "1")
        assert False, "Ожидалось исключение ValueError"
    except ValueError:
        pass


def test_cancel_request():
    employee = Employee(1, "Иванов Иван", "IT", 25)
    requests = [
        Request(
            1,
            employee,
            "Отпуск",
            "На согласовании у руководителя",
            "2026-09-15",
        )
    ]

    cancel_request(requests, 1)

    assert len(requests) == 0


def test_statistics():
    employee = Employee(1, "Иванов Иван", "IT", 25)
    requests = [
        Request(
            1,
            employee,
            "Отпуск",
            "На согласовании у руководителя",
            "2026-09-15",
        )
    ]

    statistics = get_request_statistics(requests)

    assert statistics["Отпуск"] == 1
