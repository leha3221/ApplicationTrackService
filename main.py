from datetime import date
import random


def get_data():
    fio = input("Введите ФИО сотрудника: ").strip()
    department = input("Введите подразделение: ").strip()
    age = int(input("Введите возраст сотрудника: "))
    return fio, department, age


def get_type_and_status(choice, age):
    if choice == "1":
        request_type = "Отпуск"
        status = "На согласовании у руководителя"
    elif choice == "2":
        request_type = "Перевод"
        status = "На согласовании у HR"
    elif choice == "3":
        request_type = "Увольнение"
        status = "На согласовании у HR и руководителя"
    elif choice == "4":
        request_type = "Прием на работу"
        status = "На регистрации в HR"
    else:
        request_type = "Неизвестно"
        status = "Отклонено: неверный тип заявления"

    if age < 18:
        status = "Отклонено: сотрудник младше 18 лет"
    elif age > 70:
        status = "Требуется дополнительная проверка (возраст > 70)"

    return request_type, status


def show_card(fio, department, age, request_type, status):
    number = random.randint(1000, 9999)
    today = date.today().strftime("%d.%m.%Y")

    print(f"\n     КАРТОЧКА КАДРОВОГО ЗАЯВЛЕНИЯ")
    print(f"Номер заявления : {number}")
    print(f"Дата подачи     : {today}")
    print(f"ФИО сотрудника  : {fio}")
    print(f"Подразделение   : {department}")
    print(f"Возраст         : {age} лет")
    print(f"Тип заявления   : {request_type}")
    print(f"Статус          : {status}")


print("  СЕРВИС УЧЕТА КАДРОВЫХ ЗАЯВЛЕНИЙ")

fio, department, age = get_data()
choice = input("Тип заявления (1-отпуск, 2-перевод, 3-увольнение, 4-прием): ").strip()

request_type, status = get_type_and_status(choice, age)
show_card(fio, department, age, request_type, status)