from categories import (
    get_category_name,
    find_category,
)


def test_get_category_name():
    categories = [
        {"code": "1", "name": "Отпуск"},
        {"code": "2", "name": "Перевод"},
    ]
    assert get_category_name(categories, "1") == "Отпуск"


def test_get_unknown_category():
    categories = [{"code": "1", "name": "Отпуск"}]
    assert get_category_name(categories, "99") == "Неизвестная категория"


def test_find_category():
    categories = [
        {"code": "1", "name": "Отпуск"},
        {"code": "2", "name": "Перевод"},
    ]
    result = find_category(categories, "перев")
    assert len(result) == 1
    assert result[0]["code"] == "2"
