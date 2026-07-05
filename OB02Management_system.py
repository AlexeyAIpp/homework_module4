class User:
    def __init__(self, user_id, name):
        self.__id = user_id
        self.__name = name
        self.__access_level = "user"

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        if not name.strip():
            raise ValueError("Имя не может быть пустым.")
        self.__name = name

    def get_access_level(self):
        return self.__access_level

    def _set_access_level(self, level):
        self.__access_level = level

    def __str__(self):
        return f"Сотудник(ID={self.__id}, Имя='{self.__name}', Уровень доступа='{self.__access_level}')"


class Admin(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)
        self._set_access_level("admin")

    def add_user(self, user_list, user):
        for existing_user in user_list:
            if existing_user.get_id() == user.get_id():
                raise ValueError(f"Сотрудник с ID {user.get_id()} уже существует.")
        user_list.append(user)

    def remove_user(self, user_list, user_id):
        for user in user_list:
            if user.get_id() == user_id:
                user_list.remove(user)
                return
        raise ValueError(f"Сотрудник с ID {user_id} не найден.")


# Пример использования
users = []

user1 = User(123, "Максим")
user2 = User(204, "Мария")
user3 = User(302, "Татьяна")
user4 = User(333, "Всеволод")
admin1 = Admin(777, "Алексей")

admin1.add_user(users, user1)
admin1.add_user(users, user2)
admin1.add_user(users, user3)
admin1.add_user(users, user4)
admin1.add_user(users, admin1)

for user in users:
    print(user)

print("Удаляем сотрудника с ID=123")
admin1.remove_user(users, 123)

for user in users:
    print(user)