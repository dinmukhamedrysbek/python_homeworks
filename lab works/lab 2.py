#1
check = lambda x: "положительное" if x > 0 else ("отрицательное" if x < 0 else "ноль")
#2
words = ["арбуз", "кот", "машина", "дом", "ананас"]

result = sorted(words, key=lambda w: (len(w), w[0]))
print(result)
#3
numbers = [5, 12, 7, 20, 33, 8]

result = list(filter(lambda x: x % 2 == 0 and x > 10, numbers))
print(result)
#4
numbers = [1, 2, 3, 4, 5, 6]

result = list(map(lambda x: x**2 if x % 2 == 0 else x*3, numbers))
print(result)
#5
compare = lambda a, b: "a больше" if a > b else ("b больше" if b > a else "равны")
#6
numbers = [0, -3, 5, -7, 8]

result = [(lambda x: "положительное" if x > 0 else ("отрицательное" if x < 0 else "ноль"))(x) for x in numbers]
print(result)
#генераторы 1
def even_numbers(n):
    for i in range(1, n+1):
        if i % 2 == 0:
            yield "кратно 4" if i % 4 == 0 else i
#2
def filter_words(words):
    for w in words:
        if len(w) > 4:
            yield "с а" if "а" in w else w
#3
def infinite_numbers():
    i = 1
    while True:
        if i % 15 == 0:
            yield "FizzBuzz"
        elif i % 3 == 0:
            yield "Fizz"
        elif i % 5 == 0:
            yield "Buzz"
        else:
            yield i
        i += 1
#4
def squares(n):
    for i in range(1, n+1):
        sq = i*i
        yield "чётный квадрат" if sq % 2 == 0 else sq
#Comprehension и итераторы 1
result = [x*x for x in range(1, 21) if x % 2 == 0]
#2
matrix = [[1,2,3], [4,5,6], [7,8,9]]

result = [ (lambda row: eval("*".join(map(str, row))))(row) for row in matrix ]
#3
words = ["кот", "машина", "ананас", "дом"]

result = [w for w in words if len(w) > 4 and "а" not in w]
#4
words = ["кот", "машина", "ананас", "дом"]

result = [w for w in words if len(w) > 4 and "а" not in w]
#5
words = ["кот", "машина", "ананас", "дом"]

result = [w for w in words if len(w) > 4 and "а" not in w]
#6
result = [
    "FizzBuzz" if x % 15 == 0 else
    "Fizz" if x % 3 == 0 else
    "Buzz" if x % 5 == 0 else x
    for x in range(1, 21)
]
#1
def is_prime(x):
    if x < 2:
        return False
    for i in range(2, int(x**0.5)+1):
        if x % i == 0:
            return False
    return True

def special_numbers(n):
    for i in range(1, n+1):
        if i % 15 == 0:
            yield "FizzBuzz"
        elif i % 3 == 0:
            yield "Fizz"
        elif i % 5 == 0:
            yield "Buzz"
        elif is_prime(i):
            yield "простое"
        else:
            yield i
#2
words = ["кот", "машина", "арбуз", "дом", "ананас"]

result = [
    (lambda w: (w.upper() if len(w) > 4 else "short") + ("*" if "а" in w else ""))(w)
    for w in words
]
#3
def process_numbers(numbers):
    return (
        (lambda x: x/2 if x % 2 == 0 else x*3 + 1)(x)
        for x in filter(lambda x: x >= 0, numbers)
    )
#4
students = [("Иван", 85), ("Анна", 72), ("Пётр", 90), ("Мария", 60)]

grade = lambda x: "Отлично" if x >= 90 else ("Хорошо" if x >= 70 else "Удовлетворительно")

result = {name: grade(score) for name, score in students}
#5
def matrix_transform(matrix):
    for row in matrix:
        for x in row:
            yield (
                "кратно 6" if x % 6 == 0 else
                "чётное" if x % 2 == 0 else
                "кратно 3" if x % 3 == 0 else x
            )
#1
numbers = [1,2,3,4,5]
doubled = list(map(lambda x: x*2, numbers))
#2
words = ["кот", "машина", "арбуз", "дом"]

result = list(map(lambda w: w.upper() + "!" if len(w) > 3 else w.upper(), words))
#3
words = ["кот", "машина", "арбуз", "дом"]

result = list(map(lambda w: w.upper() + "!" if len(w) > 3 else w.upper(), words))
#4
numbers = [0, 5, 12, 7, 20, -3, 8]

result = list(
    map(lambda x: x/2 if x % 2 == 0 else x*3,
        filter(lambda x: x > 5, numbers))
)