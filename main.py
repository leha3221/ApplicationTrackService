"""Точка входа в Application Track Service."""

from employees import (
    add_employee,
    find_employees,
    get_next_employee_id,
    show_employees,
)
from requests import (
    cancel_request,
    create_request,
    find_requests,
    get_request_statistics,
    show_requests,
    sort_requests,
)
from storage import (
    load_employees,
    load_requests,
    save_employees,
    save_requests,
)
from utils import input_choice, input_int, input_non_empty


def show_menu() -> None:
    """Вывести главное меню приложения."""
    print("\n=== APPLICATION TRACK SERVICE ===")
    print("1. Показать сотрудников")
    print("2. Добавить сотрудника")
    print("3. Найти сотрудника")
    print("4. Создать заявление")
    print("5. Показать заявления")
    print("6. Найти заявления")
    print("7. Отменить заявление")
    print("8. Сортировать заявления")
    print("9. Статистика")
    print("0. Выход")


def main() -> None:
    """Запустить основной цикл приложения."""
    employees = load_employees("data/employees.json")
    requests = load_requests("data/requests.json")

    while True:
        show_menu()

        choice = input_choice(
            "Выберите действие: ",
            {str(i) for i in range(10)},
        )

        if choice == "0":
            print("Работа приложения завершена.")
            break

        if choice == "1":
            show_employees(employees)

        elif choice == "2":
            fio = input_non_empty("Введите ФИО сотрудника: ")
            department = input_non_empty("Введите подразделение: ")
            age = input_int("Введите возраст сотрудника: ", 1, 120)

            employee = add_employee(
                employees,
                get_next_employee_id(employees),
                fio,
                department,
                age,
            )

            save_employees("data/employees.json", employees)
            print(f"Сотрудник добавлен. ID: {employee['id']}")

        elif choice == "3":
            query = input_non_empty(
                "Введите ФИО или подразделение для поиска: "
            )
            found = find_employees(employees, query)
            show_employees(found)

        elif choice == "4":
            employee_id = input_int("Введите ID сотрудника: ", 1)

            request_choice = input_choice(
                "Тип заявления "
                "(1-отпуск, 2-перевод, 3-увольнение, 4-прием): ",
                {"1", "2", "3", "4"},
            )

            try:
                request = create_request(
                    requests,
                    employees,
                    employee_id,
                    request_choice,
                )

                save_requests("data/requests.json", requests)

                print("\nЗаявление создано.")
                print(f"Номер заявления: {request['id']}")
                print(f"Тип: {request['type']}")
                print(f"Статус: {request['status']}")

            except ValueError as error:
                print(f"Ошибка: {error}")

        elif choice == "5":
            show_requests(requests, employees)

        elif choice == "6":
            query = input_non_empty(
                "Введите ФИО, тип или статус для поиска: "
            )
            found = find_requests(requests, employees, query)
            show_requests(found, employees)

        elif choice == "7":
            request_id = input_int("Введите номер заявления: ", 1)

            try:
                cancel_request(requests, request_id)
                save_requests("data/requests.json", requests)
                print("Заявление отменено.")
            except ValueError as error:
                print(f"Ошибка: {error}")

        elif choice == "8":
            sort_choice = input_choice(
                "Сортировка: 1 - по дате, 2 - по типу, 3 - по статусу: ",
                {"1", "2", "3"},
            )
            sorted_requests = sort_requests(requests, sort_choice)
            show_requests(sorted_requests, employees)

        elif choice == "9":
            statistics = get_request_statistics(requests)

            print("\n=== СТАТИСТИКА ===")
            print(f"Всего сотрудников: {len(employees)}")
            print(f"Всего заявлений: {len(requests)}")

            for key, value in statistics.items():
                print(f"{key}: {value}")


if __name__ == "__main__":
    main()