#1
#from flask import Flask
#app = Flask(__name__)

#class Player:
#    def __init__(self, id, name, hp):
#        self._id = id
#        self._name = name.strip().title()
#        self._hp = max(0, hp)
#    def __str__(self):
#        return f"Player(id={self._id}, name='{self._name}', hp={self._hp})"
#
#    def __del__(self):
#        print(f"Player {self._name} удалён")
#2
#class Player:
#    ...
#
#    @classmethod
#    def from_string(cls, data: str):
#        parts = [x.strip() for x in data.split(",")]
#        if len(parts) != 3:
#            raise ValueError("Invalid format")
#        return cls(int(parts[0]), parts[1], int(parts[2]))
#3
#class Item:
#    def __init__(self, id, name, power):
#        self.id = id
#        self.name = name.strip().title()
#        self.power = power

#    def __str__(self):
#        return f"Item(id={self.id}, name='{self.name}', power={self.power})"
#
#    def __hash__(self):
#        return hash(self.id)
#
#    def __eq__(self, other):
#        return isinstance(other, Item) and self.id == other.id
#4
#class Inventory:
#    def __init__(self):
#        self._items = {}
#
#    def add_item(self, item):
#        if item.id not in self._items:
#            self._items[item.id] = item
#
#    def remove_item(self, item_id):
#        self._items.pop(item_id, None)
#
#    def get_items(self):
#        return list(self._items.values())
#
#    def unique_items(self):
#        return set(self._items.values())
#
#    def to_dict(self):
#        return self._items
#5
#class Inventory:
#    ...
#
#    def get_strong_items(self, min_power):
#        return [i for i in self._items.values() if (lambda x: x.power >= min_power)(i)]
#6
#from datetime import datetime
#
#class Event:
#    def __init__(self, type, data):
#        self.type = type
#        self.data = data
#        self.timestamp = datetime.now()
#
#    def __str__(self):
#        return f"Event(type='{self.type}', data={self.data}, timestamp='{self.timestamp}')"
#7
#class Player:
#    ...
#
#    def handle_event(self, event):
#        if event.type == "ATTACK":
#            self._hp = max(0, self._hp - event.data.get("damage", 0))
#        elif event.type == "HEAL":
#            self._hp += event.data.get("heal", 0)
#        elif event.type == "LOOT":
#            item = event.data.get("item")
#            if item:
#                self._inventory.add_item(item)
#
#
#class Warrior(Player):
#    def handle_event(self, event):
#        if event.type == "ATTACK":
#            damage = int(event.data.get("damage", 0) * 0.9)
#            self._hp = max(0, self._hp - damage)
#        else:
#            super().handle_event(event)
#
#
#class Mage(Player):
#    def handle_event(self, event):
#        if event.type == "LOOT":
#            item = event.data.get("item")
#            if item:
#                item.power = int(item.power * 1.1)
#        super().handle_event(event)
#8
#class Logger:
#    @staticmethod
#    def log(event, player, filename):
#        with open(filename, "a") as f:
#            f.write(f"{event.timestamp};{player._id};{event.type};{event.data}\n")
#9
#from sched import Event


#class Logger:
#    ...
#
#    @staticmethod
#    def read_logs(filename):
#        events = []
#        with open(filename, "r") as f:
#            for line in f:
#                parts = line.strip().split(";")
#                if len(parts) != 4:
#                    continue
#                _, _, event_type, data = parts
#                events.append(Event(event_type, {"raw": data}))
#        return events
#10
#class EventIterator:
#    def __init__(self, events):
#        self.events = events
#        self.index = 0
#
#    def __iter__(self):
#        return self
#
#    def __next__(self):
#        if self.index >= len(self.events):
#            raise StopIteration
#        val = self.events[self.index]
#        self.index += 1
#        return val
#11
def damage_stream(events):
    for e in events:
        if e.type == "ATTACK":
            yield e.data.get("damage", 0)
#12
import random

def generate_events(players, items, n):
    types = ["ATTACK", "HEAL", "LOOT"]
    events = []

    for _ in range(n):
        for p in players:
            t = (lambda: random.choice(types))()

            if t == "ATTACK":
                events.append(Event("ATTACK", {"damage": random.randint(5, 30)}))
            elif t == "HEAL":
                events.append(Event("HEAL", {"heal": random.randint(5, 20)}))
            else:
                events.append(Event("LOOT", {"item": random.choice(items)}))

    return events
#13
from collections import Counter

def analyze_logs(events):
    total_damage = sum(e.data.get("damage", 0) for e in events if e.type == "ATTACK")

    counts = Counter(e.type for e in events)

    return {
        "total_damage": total_damage,
        "most_common_event": counts.most_common(1)[0][0] if counts else None
    }
#14
decide_action = lambda player: (
    "HEAL" if player._hp < 30 else
    "LOOT" if len(player._inventory.get_items()) < 2 else
    "ATTACK"
)
#16 
class Player:
    ...

    @property
    def hp(self):
        return self._hp

    @property
    def inventory(self):
        return self._inventory
#18
class Inventory:
    ...

    def __iter__(self):
        return iter(self._items.values())
#19
def analyze_inventory(inventories):
    all_items = set()
    max_item = None

    for inv in inventories:
        for item in inv:
            all_items.add(item)
            if not max_item or item.power > max_item.power:
                max_item = item

    return {
        "unique_items": all_items,
        "top_power": max_item
    }