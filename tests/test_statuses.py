from statuses import (
    get_status_name,
    find_status,
)


def test_get_status_name():
    statuses = [
        {"code": "1", "name": "На согласовании у руководителя"},
        {"code": "2", "name": "На согласовании у HR"},
    ]
    assert get_status_name(statuses, "1") == "На согласовании у руководителя"


def test_get_unknown_status():
    statuses = [{"code": "1", "name": "На согласовании у руководителя"}]
    assert get_status_name(statuses, "99") == "Неизвестный статус"


def test_find_status():
    statuses = [
        {"code": "1", "name": "На согласовании у руководителя"},
        {"code": "5", "name": "Отклонено: сотрудник младше 18 лет"},
    ]
    result = find_status(statuses, "отклонено")
    assert len(result) == 1
    assert result[0]["code"] == "5"
