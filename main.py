import datetime
import random


def get_data():
    fio = input("Введите ФИО сотрудника: ").strip()
    department = input("Введите подразделение: ").strip()
    age = int(input("Введите возраст сотрудника: "))
    return fio, department, age


def get_type_and_status(choice, age):
    if choice == "1":
        request_type, status = "Отпуск", "На согласовании у руководителя"
    elif choice == "2":
        request_type, status = "Перевод", "На согласовании у HR"
    elif choice == "3":
        request_type, status = "Увольнение", "На согласовании у HR и руководителя"
    elif choice == "4":
        request_type, status = "Прием на работу", "На регистрации в HR"
    else:
        request_type, status = "Неизвестно", "Отклонено: неверный тип заявления"

    if age < 18:
        status = "Отклонено: сотрудник младше 18 лет"
    elif age > 70:
        status = "Требуется дополнительная проверка (возраст > 70)"

    return request_type, status


def show_card(fio, department, age, request_type, status):
    number = random.randint(1000, 9999)
    date_str = datetime.date.today().strftime("%d.%m.%Y")

    print("         КАРТОЧКА КАДРОВОГО ЗАЯВЛЕНИЯ")
    print(f"Номер заявления : HR-{number}")
    print(f"Дата подачи     : {date_str}")
    print(f"ФИО сотрудника  : {fio}")
    print(f"Подразделение   : {department}")
    print(f"Возраст         : {age} лет")
    print(f"Тип заявления   : {request_type}")
    print(f"Статус          : {status}")

    if "Отклонено" in status:
        print("Заявление НЕ принято. Обратитесь в кадровую службу.")
    elif "Требуется" in status:
        print("Заявление принято. Ожидайте дополнительной проверки.")
    else:
        print("Заявление успешно зарегистрировано в системе.")


print("  СЕРВИС УЧЕТА КАДРОВЫХ ЗАЯВЛЕНИЙ")

fio, department, age = get_data()

print("\nВыберите тип заявления:")
print("1 - Отпуск")
print("2 - Перевод")
print("3 - Увольнение")
print("4 - Прием на работу")

choice = input("Введите номер типа: ").strip()

request_type, status = get_type_and_status(choice, age)

show_card(fio, department, age, request_type, status)