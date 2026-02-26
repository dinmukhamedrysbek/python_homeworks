import csv

with open("data/employees.csv", "r", encoding="utf-8") as file:
    content = file.read()
    print("Содержимое файла:")
    print(content)