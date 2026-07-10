class Animal:
    def __init__(self, species, name, age):
        self._species = species
        self._name = name
        self._age = age

    def get_species(self):
        return self._species

    def get_name(self):
        return self._name

    def get_age(self):
        return self._age

    def make_sound(self):
        return f"{self._name} издает звук."

    def eat(self):
        return f"{self._name} ест."

    def __str__(self):
        return f"{self._species} {self._name}, возраст - {self._age}"


class Bird(Animal):
    def __init__(self, species, name, age, wing_span):
        super().__init__(species, name, age)
        self._wing_span = wing_span

    def get_wing_span(self):
        return self._wing_span

    def make_sound(self):
        return f"{self._species} {self._name} произносит: Чирик!"


class Mammal(Animal):
    def __init__(self, species, name, age, fur_color):
        super().__init__(species, name, age)
        self._fur_color = fur_color

    def get_fur_color(self):
        return self._fur_color

    def make_sound(self):
        return f"{self._species} {self._name} произносит: Р-р-р!"


class Reptile(Animal):
    def __init__(self, species, name, age, is_venomous):
        super().__init__(species, name, age)
        self._is_venomous = is_venomous

    def get_is_venomous(self):
        return self._is_venomous

    def make_sound(self):
        return f"{self._species} {self._name} произносит: Ш-ш-ш!"


def animal_sound(animals):
    for animal in animals:
        print(animal.make_sound())


class Employee:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name


class ZooKeeper(Employee):
    def feed_animal(self, animal):
        return f"{self._name} кормит {animal.get_name()}. {animal.eat()}"

    def __str__(self):
        return f"Смотритель зоопарка - {self._name}"


class Veterinarian(Employee):
    def heal_animal(self, animal):
        return f"{self._name} лечит {animal.get_name()}."

    def __str__(self):
        return f"Ветеринар - {self._name}"


class Zoo:
    def __init__(self, name):
        self._name = name
        self._animals = []
        self._employees = []

    def add_animal(self, animal):
        self._animals.append(animal)

    def add_employee(self, employee):
        self._employees.append(employee)

    def get_animals(self):
        return self._animals

    def get_employees(self):
        return self._employees

    def show_animals(self):
        print(f"Животные в зоопарке '{self._name}':")
        for animal in self._animals:
            print(animal)

    def show_employees(self):
        print(f"Сотрудники зоопарка '{self._name}':")
        for employee in self._employees:
            print(employee)

    def save_to_file(self, filename):
        with open(filename, "w", encoding="utf-8") as file:
            file.write(self._name + "\n")
            file.write("ЖИВОТНЫЕ\n")

            for animal in self._animals:
                if isinstance(animal, Bird):
                    file.write(f"Птица;{animal._species};{animal._name};{animal._age};{animal._wing_span}\n")
                elif isinstance(animal, Mammal):
                    file.write(f"Млекопитающее;{animal._species};{animal._name};{animal._age};{animal._fur_color}\n")
                elif isinstance(animal, Reptile):
                    file.write(f"Пресмыкающееся;{animal._species};{animal._name};{animal._age};{animal._is_venomous}\n")

            file.write("СОТРУДНИКИ\n")

            for employee in self._employees:
                if isinstance(employee, ZooKeeper):
                    file.write(f"Смотритель зоопарка;{employee._name}\n")
                elif isinstance(employee, Veterinarian):
                    file.write(f"Ветеринар;{employee._name}\n")

    def load_from_file(self, filename):
        self._animals = []
        self._employees = []

        with open(filename, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.strip()]

        self._name = lines[0]
        mode = ""

        for line in lines[1:]:
            if line == "ЖИВОТНЫЕ":
                mode = "animals"
                continue

            if line == "СОТРУДНИКИ":
                mode = "employees"
                continue

            parts = line.split(";")

            if mode == "animals":
                animal_type = parts[0]
                species = parts[1]
                name = parts[2]
                age = int(parts[3])

                animal = None

                if animal_type == "Птица":
                    animal = Bird(species, name, age, float(parts[4]))
                elif animal_type == "Млекопитающее":
                    animal = Mammal(species, name, age, parts[4])
                elif animal_type == "Пресмыкающееся":
                    animal = Reptile(species, name, age, parts[4] == "True")

                if animal is not None:
                    self.add_animal(animal)

            elif mode == "employees":
                employee_type = parts[0]
                name = parts[1]

                employee = None

                if employee_type == "Смотритель зоопарка":
                    employee = ZooKeeper(name)
                elif employee_type == "Ветеринар":
                    employee = Veterinarian(name)

                if employee is not None:
                    self.add_employee(employee)


# Пример использования
parrot = Bird("Попугай", "Кеша", 2, 0.4)
tiger = Mammal("Тигр", "Амур", 5, "оранжевый")
snake = Reptile("Змея", "Шип", 4, True)

animals = [parrot, tiger, snake]

print("Демонстрация полиморфизма:")
animal_sound(animals)

keeper = ZooKeeper("Иван")
vet = Veterinarian("Ольга")

zoo = Zoo("Центральный")
zoo.add_animal(parrot)
zoo.add_animal(tiger)
zoo.add_animal(snake)

zoo.add_employee(keeper)
zoo.add_employee(vet)

zoo.save_to_file("zoo_data.txt")

print("\nДанные сохранены в файл.\n")

new_zoo = Zoo("")
new_zoo.load_from_file("zoo_data.txt")

new_zoo.show_animals()
print()
new_zoo.show_employees()
print()
animal_sound(new_zoo.get_animals())
print()

loaded_keeper = new_zoo.get_employees()[0]
loaded_vet = new_zoo.get_employees()[1]
loaded_tiger = new_zoo.get_animals()[1]
loaded_snake = new_zoo.get_animals()[2]

print(loaded_keeper.feed_animal(loaded_tiger))
print(loaded_vet.heal_animal(loaded_snake))