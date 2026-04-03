#1
class User:
    def __init__(self, id, name, email):
        self._id = id
        self._name = name.strip().title()
        email = email.strip().lower()
        if "@" not in email:
            raise ValueError("Invalid email")
        self._email = email

    def __str__(self):
        return f"User(id={self._id}, name='{self._name}', email='{self._email}')"

    def __del__(self):
        print(f"User {self._name} deleted")


#2
class User:
    ...

    @classmethod
    def from_string(cls, data: str):
        parts = [x.strip() for x in data.split(",")]
        if len(parts) != 3:
            raise ValueError("Invalid format")
        return cls(int(parts[0]), parts[1], parts[2])


#3
class Product:
    def __init__(self, id, name, price, category):
        self.id = id
        self.name = name
        self.price = float(price)
        self.category = category

    def __str__(self):
        return f"Product(id={self.id}, name='{self.name}', price={self.price}, category='{self.category}')"

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Product) and self.id == other.id

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price, "category": self.category}


#4
class Inventory:
    def __init__(self):
        self._products = {}

    def add_product(self, product):
        if product.id not in self._products:
            self._products[product.id] = product

    def remove_product(self, product_id):
        self._products.pop(product_id, None)

    def get_product(self, product_id):
        return self._products.get(product_id)

    def get_all_products(self):
        return list(self._products.values())

    def unique_products(self):
        return set(self._products.values())

    def to_dict(self):
        return self._products


#5
class Inventory:
    ...

    def filter_by_price(self, min_price):
        return [p for p in self._products.values() if (lambda x: x.price >= min_price)(p)]


#6
from datetime import datetime

class Logger:
    @staticmethod
    def log_action(user, action, product, filename):
        with open(filename, "a") as f:
            f.write(f"{datetime.now()};{user._id};{action};{product.id}\n")

    @staticmethod
    def read_logs(filename):
        result = []
        with open(filename, "r") as f:
            for line in f:
                t, uid, act, pid = line.strip().split(";")
                result.append({
                    "timestamp": t,
                    "user_id": int(uid),
                    "action": act,
                    "product_id": int(pid)
                })
        return result


#7
class Order:
    def __init__(self, id, user, products=None):
        self.id = id
        self.user = user
        self.products = products if products else []

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product_id):
        self.products = [p for p in self.products if p.id != product_id]

    def total_price(self):
        return sum(p.price for p in self.products)

    def __str__(self):
        return f"Order(id={self.id}, user={self.user._name}, total={self.total_price()})"


#8
class Order:
    ...

    def most_expensive_products(self, n):
        return sorted(self.products, key=lambda x: x.price, reverse=True)[:n]


#9
def price_stream(products):
    for p in products:
        yield p.price


#10
class OrderIterator:
    def __init__(self, orders):
        self.orders = orders
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.orders):
            raise StopIteration
        val = self.orders[self.index]
        self.index += 1
        return val


#11
import numpy as np

def prices_array(products):
    return np.array([p.price for p in products], dtype=float)


#12
def stats_prices(arr):
    return (arr.mean(), np.median(arr))


#13
def normalize_prices(arr):
    return (arr - arr.min()) / (arr.max() - arr.min())


#14
def categories_array(products):
    return np.array([p.category for p in products])


#15
def unique_categories(arr):
    return len(set(arr))


#16
def above_mean_products(products):
    arr = prices_array(products)
    mean = arr.mean()
    return [p for p in products if p.price > mean]


#17
def discount(arr):
    return arr * 0.9


#18
def orders_matrix(orders):
    return np.array([[o.total_price()] for o in orders])


#19
def avg_order(arr):
    return arr.mean()


#20
def expensive_indexes(arr):
    return list(np.where(arr > 1000)[0])


#21
import pandas as pd
from datetime import date

def users_df(users):
    return pd.DataFrame([{
        "id": u._id,
        "name": u._name,
        "email": u._email,
        "registration_date": date.today()
    } for u in users])


#22
def products_df(products):
    return pd.DataFrame([p.to_dict() for p in products])


#23
def merge_users_orders(users_df, orders_df):
    df = pd.merge(users_df, orders_df, left_on="id", right_on="user_id")
    return df[["order_id", "name", "total"]].rename(columns={"name": "user_name"})


#24
def filter_orders(df, value):
    return df[df["total"] > value]


#25
def sum_by_user(df):
    return df.groupby("user_name")["total"].sum().reset_index(name="total_sum")


#26
def mean_by_user(df):
    return df.groupby("user_name")["total"].mean().reset_index(name="mean_total")


#27
def count_orders(df):
    return df.groupby("user_name")["total"].count().reset_index(name="orders_count")


#28
def mean_price_category(df):
    return df.groupby("category")["price"].mean().reset_index(name="mean_price")


#29
def add_discount(df):
    df["discounted_price"] = df["price"] * 0.9
    return df


#30
def sort_products(df):
    return df.sort_values(by="price", ascending=False)


#31
def add_quantity(df):
    df["quantity"] = 1
    return df


#32
def total_price(df):
    df["total_price"] = df["price"] * df["quantity"]
    return df


#33
def filter_category(df):
    return df[df["category"] == "Electronics"]


#34
def count_category(df):
    return df.groupby("category").size().reset_index(name="count")


#35
def mean_category(df):
    return df.groupby("category")["price"].mean().reset_index(name="mean_price")


#36
def sort_orders(df):
    return df.sort_values(by="total_price", ascending=False)


#37
def top_orders(df):
    return df.sort_values(by="total_price", ascending=False).head(3)


#38
def merge_orders_users(df1, df2):
    return pd.merge(df2, df1, on="user_id")[["order_id", "user_name", "total_price"]]


#39
def avg_user(df):
    return df.groupby("user_name")["total_price"].mean().reset_index(name="mean_total")


#40
def count_user(df):
    return df.groupby("user_name")["order_id"].count().reset_index(name="orders_count")


#41
def max_order(df):
    return df.groupby("user_name")["total_price"].max().reset_index(name="max_order")


#42
def unique_cat_user(df):
    return df.groupby("user_name")["category"].nunique().reset_index(name="unique_categories")


#43
def add_vip(df):
    df["VIP"] = df["total_sum"] > 1000
    return df


#44
def sort_users(df):
    return df.sort_values(by=["total_sum", "mean_total"], ascending=[False, True])


#45
def final_report(df):
    result = df.groupby("user_name").agg(
        total_orders=("order_id", "count"),
        total_sum=("total_price", "sum"),
        mean_total=("total_price", "mean"),
        max_order=("total_price", "max"),
        unique_categories=("category", "nunique")
    ).reset_index()

    result["VIP"] = result["total_sum"] > 1000
    return result