from statuses import Status, find_status, get_status_name


def test_status_creation():
    status = Status("1", "На согласовании у руководителя")

    assert status.code == "1"
    assert status.name == "На согласовании у руководителя"


def test_status_str():
    status = Status("1", "На согласовании у руководителя")

    assert str(status) == "1. На согласовании у руководителя"


def test_get_status_name():
    statuses = [
        Status("1", "На согласовании у руководителя"),
        Status("2", "На согласовании у HR"),
    ]
    assert get_status_name(statuses, "1") == "На согласовании у руководителя"


def test_get_unknown_status():
    statuses = [Status("1", "На согласовании у руководителя")]
    assert get_status_name(statuses, "99") == "Неизвестный статус"


def test_find_status():
    statuses = [
        Status("1", "На согласовании у руководителя"),
        Status("5", "Отклонено: сотрудник младше 18 лет"),
    ]
    result = find_status(statuses, "отклонено")
    assert len(result) == 1
    assert result[0].code == "5"
