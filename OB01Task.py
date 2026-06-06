class Task:
    def __init__(self, description, due_date, completed=False):
        self.description = description
        self.due_date = due_date
        self.completed = completed


tasks = []


def add_task():
    description = input("Введите описание задачи: ")
    due_date = input("Введите срок выполнения: ")
    tasks.append(Task(description, due_date))
    print("Задача добавлена.")


def show_current_tasks():
    current = [task for task in tasks if not task.completed]

    print("\nТекущие задачи:")
    if not current:
        print("Нет невыполненных задач.")
    else:
        for i, task in enumerate(current, start=1):
            print(f"{i}. {task.description} — срок: {task.due_date}")

    return current


def complete_task():
    current = show_current_tasks()

    if not current:
        return

    index = int(input("Введите номер выполненной задачи: ")) - 1

    if 0 <= index < len(current):
        current[index].completed = True
        print("Задача отмечена как выполненная.")
    else:
        print("Неверный номер задачи.")


while True:
    print("\nМеню:")
    print("1. Добавить задачу")
    print("2. Отметить задачу выполненной")
    print("3. Показать текущие задачи")
    print("4. Выход")

    choice = input("Выберите действие: ")

    if choice == "1":
        add_task()
    elif choice == "2":
        complete_task()
    elif choice == "3":
        show_current_tasks()
    elif choice == "4":
        print("Выход из программы.")
        break
    else:
        print("Неверный выбор. Попробуйте снова.")