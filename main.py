import datetime
import random


print("  СЕРВИС УЧЕТА КАДРОВЫХ ЗАЯВЛЕНИЙ")


fio = input("Введите ФИО сотрудника: ").strip()
department = input("Введите подразделение: ").strip()

age_input = input("Введите возраст сотрудника: ")
age = int(age_input)

print("\nВыберите тип заявления:")
print("1 - Отпуск")
print("2 - Перевод")
print("3 - Увольнение")
print("4 - Прием на работу")

choice = input("Введите номер типа: ").strip()

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
else:
    pass

request_number = random.randint(1000, 9999)
today = datetime.date.today()
date_str = today.strftime("%d.%m.%Y")


print("         КАРТОЧКА КАДРОВОГО ЗАЯВЛЕНИЯ")
print(f"Номер заявления : HR-{request_number}")
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