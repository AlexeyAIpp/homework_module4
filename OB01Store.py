class Store:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.items = {}

    def add_item(self, item_name, price):
        self.items[item_name] = price
        print(f"Товар '{item_name}' добавлен по цене {price}.")

    def remove_item(self, item_name):
        removed = self.items.pop(item_name, None)
        if removed is None:
            print(f"Товар '{item_name}' не найден.")
        else:
            print(f"Товар '{item_name}' удален.")

    def get_price(self, item_name):
        return self.items.get(item_name)

    def update_price(self, item_name, new_price):
        if item_name in self.items:
            self.items[item_name] = new_price
            print(f"Цена товара '{item_name}' обновлена: {new_price}")
        else:
            print(f"Товар '{item_name}' не найден.")

    def show_items(self):
        print(f"\nМагазин: {self.name}")
        print(f"Адрес: {self.address}")
        if not self.items:
            print("Ассортимент пуст.")
        else:
            print("Ассортимент:")
            for item, price in self.items.items():
                print(f"- {item}: {price}")
#Создание магазинов:
store1 = Store("Фруктовый рай", "ул. Ленина, 10")
store2 = Store("ТехноМир", "пр. Победы, 25")
store3 = Store("Домашний уют", "ул. Садовая, 7")

#Добавление товаров в магазины:
store1.add_item("яблоки", 100)
store1.add_item("бананы", 120)
store1.add_item("апельсины", 90)

store2.add_item("ноутбук", 50000)
store2.add_item("мышка", 1500)

store3.add_item("стол", 7000)
store3.add_item("лампа", 2500)

#Тестирование методов на примере магазина "Фруктовый рай":
print(f"Товары магазина '{store1.name}': {store1.items}")

#Добавление товара:
store1.add_item("груши", 130)
print("После добавления:", store1.items)

#Обновление цены:
store1.update_price("яблоки", 110)
print("После изменения цены:", store1.items)

#Удаление товара:
store1.remove_item("бананы")
print("После удаления:", store1.items)

#Вывод цены по названию товара:
item_name = input("Введите название товара: ")
price = store1.get_price(item_name)
if price is not None:
    print(f"Цена товара '{item_name}': {price}")
else:
    print("Такого товара нет.")