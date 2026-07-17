from abc import ABC, abstractmethod


class Weapon(ABC):
    @abstractmethod
    def attack(self):
        pass

    @property
    @abstractmethod
    def name_ru(self):
        pass


class Sword(Weapon):
    @property
    def name_ru(self):
        return "меч"

    def attack(self):
        return "Боец наносит удар мечом."


class Bow(Weapon):
    @property
    def name_ru(self):
        return "лук"

    def attack(self):
        return "Боец наносит удар из лука."


class Axe(Weapon):
    @property
    def name_ru(self):
        return "топор"

    def attack(self):
        return "Боец наносит удар топором."


class Monster:
    def __init__(self, name):
        self.name = name
        self.is_alive = True

    def defeat(self):
        self.is_alive = False


class Fighter:
    def __init__(self, name, weapon=None):
        self.name = name
        self.weapon = weapon

    def change_weapon(self, weapon):
        self.weapon = weapon
        print(f"{self.name} выбирает {weapon.name_ru}.")

    def attack_monster(self, monster):
        if self.weapon is None:
            print(f"{self.name} без оружия и не может атаковать!")
            return

        print(self.weapon.attack())
        monster.defeat()
        print(f"{monster.name} побежден!")


def battle_demo():
    fighter = Fighter("Боец")

    monster1 = Monster("Монстр")
    fighter.change_weapon(Sword())
    fighter.attack_monster(monster1)

    print()

    monster2 = Monster("Монстр")
    fighter.change_weapon(Bow())
    fighter.attack_monster(monster2)

    print()

    monster3 = Monster("Монстр")
    fighter.change_weapon(Axe())
    fighter.attack_monster(monster3)


if __name__ == "__main__":
    battle_demo()