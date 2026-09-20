from requests import (
    create_request,
    get_request_statistics,
    get_type_and_status,
)


def test_get_type_and_status():
    request_type, status = get_type_and_status("1", 25)

    assert request_type == "Отпуск"
    assert status == "На согласовании у руководителя"


def test_minor_employee():
    _, status = get_type_and_status("1", 17)

    assert status == "Отклонено: сотрудник младше 18 лет"


def test_create_request():
    employees = [
        {"id": 1, "fio": "Иванов Иван", "department": "IT", "age": 25}
    ]
    requests = []

    request = create_request(requests, employees, 1, "1")

    assert request["id"] == 1
    assert len(requests) == 1


def test_statistics():
    requests = [
        {
            "id": 1,
            "employee_id": 1,
            "type": "Отпуск",
            "status": "На согласовании у руководителя",
            "date": "2026-09-15",
        }
    ]

    statistics = get_request_statistics(requests)

    assert statistics["Отпуск"] == 1
