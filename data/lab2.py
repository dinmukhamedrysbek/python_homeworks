#task 1 
unique_users = set()
total_purchases = 0
total_sum = 0
user_spending = {}
# Читаем файл
with open("data/shop.txt", "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()

        if not line:
            continue

        parts = line.split(";")

        if len(parts) < 3:
            continue

        user = parts[1]
        action = parts[2]

        unique_users.add(user)

        if action == "BUY":
            if len(parts) < 4:
                continue

            amount = int(parts[3])
            total_purchases += 1
            total_sum += amount

            if user not in user_spending:
                user_spending[user] = 0

            user_spending[user] += amount
# Ищем пользователя с максимальной суммой
max_user = ""
max_spent = 0
for user in user_spending:
    if user_spending[user] > max_spent:
        max_spent = user_spending[user]
        max_user = user
# Считаем средний чек
if total_purchases > 0:
    average_check = total_sum / total_purchases
else:
    average_check = 0
# Записываем результат в файл
with open("data/report.txt", "w", encoding="utf-8") as report:
    report.write("Уникальных пользователей: " + str(len(unique_users)) + "\n")
    report.write("Всего покупок: " + str(total_purchases) + "\n")
    report.write("Общая сумма: " + str(total_sum) + "\n")
    report.write("Самый активный покупатель: " + max_user + "\n")
    report.write("Средний чек: " + str(average_check) + "\n")

#task 2
import csv

employees = []                 # список сотрудников
department_salaries = {}       # словарь для отделов
total_salary = 0
total_count = 0

# Читаем файл
with open("data/employees.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        name = row["name"]
        department = row["department"]
        salary = int(row["salary"])

        employees.append(row)

        total_salary += salary
        total_count += 1

        # Группировка по отделам
        if department not in department_salaries:
            department_salaries[department] = []

        department_salaries[department].append(salary)

# Средняя зарплата
average_salary = total_salary / total_count

# Средняя зарплата по отделам
department_averages = {}
for dept in department_salaries:
    salaries = department_salaries[dept]
    department_averages[dept] = sum(salaries) / len(salaries)

# Отдел с самой высокой средней зарплатой
best_department = max(department_averages, key=department_averages.get)

# Самый высокооплачиваемый сотрудник
highest_paid = max(employees, key=lambda x: int(x["salary"]))

# Сотрудники выше средней зарплаты
high_salary_employees = []

for emp in employees:
    if int(emp["salary"]) > average_salary:
        high_salary_employees.append(emp)

# Создаём новый CSV файл
with open("data/high_salary.csv", "w", newline="", encoding="utf-8") as file:
    fieldnames = ["name", "department", "salary"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(high_salary_employees)

# Вывод в консоль
print("Средняя зарплата:", average_salary)
print("Средняя зарплата по отделам:", department_averages)
print("Отдел с самой высокой средней зарплатой:", best_department)
print("Самый высокооплачиваемый сотрудник:", highest_paid["name"])
print("Сотрудники выше средней:", [emp["name"] for emp in high_salary_employees])

#task 3
import json

# Читаем JSON файл
with open("data/orders.json", "r", encoding="utf-8") as file:
    orders = json.load(file)

total_revenue = 0
user_orders = {}        # сколько заказов сделал каждый пользователь
item_counts = {}        # сколько раз встречается каждый товар

max_order_total = 0
top_user = ""

for order in orders:
    total_revenue += order["total"]

    user = order["user"]
    user_orders[user] = user_orders.get(user, 0) + 1

    # считаем товары
    for item in order["items"]:
        item_counts[item] = item_counts.get(item, 0) + 1

    # проверяем самый дорогой заказ
    if order["total"] > max_order_total:
        max_order_total = order["total"]
        top_user = user

# самый популярный товар
most_popular_item = max(item_counts, key=item_counts.get)

# создаём summary.json
summary = {
    "total_revenue": total_revenue,
    "top_user": top_user,
    "most_popular_item": most_popular_item,
    "total_orders": len(orders)
}

with open("data/summary.json", "w", encoding="utf-8") as file:
    json.dump(summary, file, ensure_ascii=False, indent=2)

# выводим для проверки
print(summary)

#task 4
import csv
import json

transactions_file = "transactions.csv"

suspicious_transactions = []  # все транзакции > 500000
user_operations = {}           # количество операций каждого пользователя

# Читаем CSV
with open("data/" + transactions_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        user = row["user_id"]
        amount = int(row["amount"])

        # считаем количество операций
        if user not in user_operations:
            user_operations[user] = 0
        user_operations[user] += 1

        # проверяем подозрительную транзакцию
        if amount > 500000:
            suspicious_transactions.append({"user": user, "amount": amount})

# Находим подозрительных пользователей (более 3 операций)
suspicious_users = set()

for user, count in user_operations.items():
    if count > 3:
        suspicious_users.add(user)

# Добавляем пользователей, которые сделали подозрительные транзакции
for trans in suspicious_transactions:
    suspicious_users.add(trans["user"])

# Общая сумма подозрительных операций
total_suspicious_amount = sum(t["amount"] for t in suspicious_transactions)

# Создаём txt отчёт
with open("data/fraud_report.txt", "w", encoding="utf-8") as report:
    report.write(f"Подозрительных транзакций: {len(suspicious_transactions)}\n")
    report.write(f"Подозрительных пользователей: {len(suspicious_users)}\n")
    report.write(f"Список пользователей: {', '.join(suspicious_users)}\n")
    report.write(f"Общая сумма подозрительных операций: {total_suspicious_amount}\n")

# Создаём JSON файл с подозрительными пользователями
with open("data/fraud_users.json", "w", encoding="utf-8") as fjson:
    json.dump(list(suspicious_users), fjson, ensure_ascii=False, indent=2)

# Для проверки
print("Подозрительные транзакции:", suspicious_transactions)
print("Подозрительные пользователи:", suspicious_users)
print("Общая сумма подозрительных операций:", total_suspicious_amount)