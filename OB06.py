import random


class Hero:

    def __init__(self, name, hero_class, health, attack_min, attack_max, potions=2):
        self.name = name
        self.hero_class = hero_class
        self.max_health = health
        self.health = health
        self.attack_min = attack_min
        self.attack_max = attack_max
        self.potions = potions
        self.shield_active = False
        self.shield_reduction = 0.5

    def is_alive(self):
        return self.health > 0

    def show_status(self):
        shield_text = "активен" if self.shield_active else "нет"
        print(
            f"{self.name} ({self.hero_class}) | "
            f"HP: {self.health}/{self.max_health} | "
            f"Зелья: {self.potions} | Щит: {shield_text}"
        )

    def take_damage(self, damage):
        if self.shield_active:
            reduced_damage = max(1, round(damage * (1 - self.shield_reduction)))
            print(f"Щит {self.name} ослабляет урон: {damage} -> {reduced_damage}.")
            damage = reduced_damage
            self.shield_active = False

        self.health = max(0, self.health - damage)
        return damage

    def attack(self, other):
        damage = random.randint(self.attack_min, self.attack_max)
        critical_chance = 20
        is_critical = random.randint(1, 100) <= critical_chance

        if is_critical:
            damage *= 2
            print(f"\nКРИТИЧЕСКИЙ УДАР! {self.name} наносит двойной урон!")
        else:
            print(f"\n{self.name} атакует героя {other.name}.")

        actual_damage = other.take_damage(damage)
        print(f"Нанесено урона: {actual_damage}.")
        print(f"Здоровье {other.name}: {other.health}/{other.max_health}.")

    def heal(self):
        if self.potions <= 0:
            print("Зелья закончились. Лечение невозможно.")
            return False

        if self.health == self.max_health:
            print("Здоровье уже полное. Зелье не потрачено.")
            return False

        heal_amount = random.randint(18, 30)
        old_health = self.health
        self.health = min(self.max_health, self.health + heal_amount)
        restored = self.health - old_health
        self.potions -= 1

        print(f"\n{self.name} использует зелье и восстанавливает {restored} HP.")
        print(f"Здоровье {self.name}: {self.health}/{self.max_health}. Зелий осталось: {self.potions}.")
        return True

    def defend(self):
        self.shield_active = True
        print(f"\n{self.name} поднимает щит. Следующий урон будет уменьшен на 50%.")


class Warrior(Hero):

    def __init__(self, name):
        super().__init__(
            name=name,
            hero_class="Воин",
            health=120,
            attack_min=18,
            attack_max=30,
            potions=2,
        )


class Mage(Hero):

    def __init__(self, name):
        super().__init__(
            name=name,
            hero_class="Маг",
            health=90,
            attack_min=15,
            attack_max=36,
            potions=3,
        )


class Archer(Hero):

    def __init__(self, name):
        super().__init__(
            name=name,
            hero_class="Лучник",
            health=100,
            attack_min=17,
            attack_max=28,
            potions=2,
        )

    def attack(self, other):
        damage = random.randint(self.attack_min, self.attack_max)
        critical_chance = 30
        is_critical = random.randint(1, 100) <= critical_chance

        if is_critical:
            damage *= 2
            print(f"\nТОЧНЫЙ ВЫСТРЕЛ! {self.name} наносит двойной урон!")
        else:
            print(f"\n{self.name} стреляет в героя {other.name}.")

        actual_damage = other.take_damage(damage)
        print(f"Нанесено урона: {actual_damage}.")
        print(f"Здоровье {other.name}: {other.health}/{other.max_health}.")


class Game:

    def __init__(self):
        self.player = None
        self.computer = None
        self.round_number = 1

    @staticmethod
    def create_hero(name, choice):
        heroes = {
            "1": Warrior,
            "2": Mage,
            "3": Archer,
        }
        return heroes[choice](name)

    def choose_player_hero(self):
        print("\nВыберите героя:")
        print("1 — Воин: 120 HP, урон 18–30, 2 зелья")
        print("2 — Маг: 90 HP, урон 15–36, 3 зелья")
        print("3 — Лучник: 100 HP, урон 17–28, шанс критического удара 30%")

        name = input("\nВведите имя героя: ").strip()
        if not name:
            name = "Герой"

        while True:
            choice = input("Введите номер класса (1–3): ").strip()
            if choice in ("1", "2", "3"):
                self.player = self.create_hero(name, choice)
                break
            print("Ошибка: введите 1, 2 или 3.")

        print(f"\nВы выбрали: {self.player.name} — {self.player.hero_class}.")

    def create_computer_hero(self):
        choice = random.choice(["1", "2", "3"])
        computer_names = ["Теневой Рыцарь", "Мастер Пламени", "Сокол Ночи", "Железный Страж"]
        name = random.choice(computer_names)
        self.computer = self.create_hero(name, choice)
        print(f"Компьютер выбрал героя: {self.computer.name} — {self.computer.hero_class}.")

    def show_battle_status(self):
        print("\n" + "=" * 58)
        print("СОСТОЯНИЕ ГЕРОЕВ")
        print("=" * 58)
        self.player.show_status()
        self.computer.show_status()
        print("=" * 58)

    def player_turn(self):
        while True:
            print("\nВаш ход:")
            print("1 — Атаковать")
            print("2 — Использовать зелье здоровья")
            print("3 — Поставить щит")

            action = input("Выберите действие (1–3): ").strip()

            if action == "1":
                self.player.attack(self.computer)
                return
            if action == "2":
                if self.player.heal():
                    return
            elif action == "3":
                self.player.defend()
                return
            else:
                print("Ошибка: введите 1, 2 или 3.")

    def computer_turn(self):
        print(f"\nХод компьютера: {self.computer.name}.")

        if self.computer.health <= 35 and self.computer.potions > 0:
            action = "heal"
        elif not self.computer.shield_active and random.randint(1, 100) <= 20:
            action = "defend"
        else:
            action = "attack"

        if action == "heal":
            self.computer.heal()
        elif action == "defend":
            self.computer.defend()
        else:
            self.computer.attack(self.player)

    def announce_winner(self):
        print("\n" + "=" * 58)
        print("БОЙ ОКОНЧЕН")
        print("=" * 58)

        if self.player.is_alive():
            print(f"Победитель: {self.player.name} ({self.player.hero_class})!")
            print(f"Осталось здоровья: {self.player.health}/{self.player.max_health}.")
        else:
            print(f"Победитель: {self.computer.name} ({self.computer.hero_class})!")
            print(f"Осталось здоровья: {self.computer.health}/{self.computer.max_health}.")

    def start(self):
        print("=" * 58)
        print("        ДОБРО ПОЖАЛОВАТЬ В «БИТВУ ГЕРОЕВ:»   ")
        print("=" * 58)

        self.choose_player_hero()
        self.create_computer_hero()
        self.show_battle_status()

        while self.player.is_alive() and self.computer.is_alive():
            print(f"\n{'-' * 22} РАУНД {self.round_number} {'-' * 22}")
            self.player_turn()

            if not self.computer.is_alive():
                break

            self.computer_turn()

            if self.player.is_alive() and self.computer.is_alive():
                self.show_battle_status()

            self.round_number += 1

        self.announce_winner()


def main():
    while True:
        game = Game()
        game.start()

        again = input("\nСыграть ещё раз? (д/н): ").strip().lower()
        if again not in ("д", "да", "y", "yes"):
            print("\nСпасибо за игру! До новых сражений!")
            break


if __name__ == "__main__":
    main()