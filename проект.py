class TreeNode:
    def __init__(self, value, amount=0):
        self.value = value
        self.amount = amount
        self.children = []

    def find_child(self, value):
        for child in self.children:
            if child.value == value:
                return child
        return None

    def add_child(self, value, amount=0):
        child = self.find_child(value)
        if child is None:
            child = TreeNode(value, amount)
            self.children.append(child)
        return child

    def print_tree(self, level=0):
        indent = "  " * level
        if isinstance(self.value, int):
            text = f"День {self.value}"
        else:
            text = str(self.value)
        if self.amount > 0:
            text += f" - {self.amount} руб."
        print(indent + text)
        for child in self.children:
            child.print_tree(level + 1)


class DailySpending:
    def __init__(self):
        self.days = [0] * 31
        self.pref_sum = [0] * 31
        self.types_of_sp = {}
        self.actions = []
        self.root = TreeNode("Месяц")

    def money(self, value):
        return str(value) + " руб."

    def checking(self, amount, day):
        return amount > 0 and 1 <= day <= 31

    def update_pref_sum(self):
        counter = 0
        for i in range(31):
            counter += self.days[i]
            self.pref_sum[i] = counter

    def add_spending(self, amount, day, categ="Без категории"):
        categ = str(categ).strip()
        if categ == "":
            categ = "Без категории"
        if not self.checking(amount, day):
            print("Некорректные данные. День должен быть от 1 до 31, сумма не меньше 0")
            return False
        self.days[day - 1] += amount
        if categ in self.types_of_sp:
            self.types_of_sp[categ] += amount
        else:
            self.types_of_sp[categ] = amount
        day_node = self.root.add_child(day)
        category_node = day_node.add_child(categ)
        expense_node = TreeNode("Расход", amount)
        category_node.children.append(expense_node)
        self.root.amount += amount
        day_node.amount += amount
        category_node.amount += amount
        self.actions.append((day, amount, categ, day_node, category_node, expense_node))
        self.update_pref_sum()
        print(f"Добавлено: день {day}, сумма {self.money(amount)}, категория: {categ}")
        return True

    def undo_last(self):
        if len(self.actions) == 0:
            print("Стек пуст. Отменять нечего")
            return False
        day, amount, categ, day_node, category_node, expense_node = self.actions.pop()
        self.days[day - 1] -= amount
        self.types_of_sp[categ] -= amount
        if self.types_of_sp[categ] <= 0:
            del self.types_of_sp[categ]
        self.root.amount -= amount
        day_node.amount -= amount
        category_node.amount -= amount
        if expense_node in category_node.children:
            category_node.children.remove(expense_node)
        if category_node.amount <= 0 and category_node in day_node.children:
            day_node.children.remove(category_node)
        if day_node.amount <= 0 and day_node in self.root.children:
            self.root.children.remove(day_node)
        self.update_pref_sum()
        print(f"Отменено: день {day}, сумма {self.money(amount)}, категория: {categ}")
        return True

    def sum_from_to(self, day_A, day_B):
        if not (1 <= day_A <= 31 and 1 <= day_B <= 31):
            print("Некорректная дата. День должен быть от 1 до 31")
            return None
        if day_A > day_B:
            day_A, day_B = day_B, day_A
        if day_A == 1:
            result = self.pref_sum[day_B - 1]
        else:
            result = self.pref_sum[day_B - 1] - self.pref_sum[day_A - 2]
        print(f"Расходы с {day_A} по {day_B} день: {self.money(result)}")
        return result

    def max_spending(self):
        max_amount = self.days[0]
        max_day = 1
        for i in range(1, len(self.days)):
            if self.days[i] > max_amount:
                max_amount = self.days[i]
                max_day = i + 1
        if max_amount == 0:
            print("Пока расходов нет")
        else:
            print(f"День с максимальным расходом: {max_day}, сумма: {self.money(max_amount)}")
        return max_day, max_amount

    def insertion_sort_categories(self):
        sp = []
        for key in self.types_of_sp:
            sp.append((key, self.types_of_sp[key]))
        for i in range(1, len(sp)):
            current = sp[i]
            j = i - 1
            while j >= 0 and sp[j][1] < current[1]:
                sp[j + 1] = sp[j]
                j -= 1
            sp[j + 1] = current
        return sp

    def show_categories_sorted(self):
        sorted_sp = self.insertion_sort_categories()
        if len(sorted_sp) == 0:
            print("Категорий пока нет")
            return
        print("\nКатегории по сумме трат:")
        for i, item in enumerate(sorted_sp, start=1):
            print(f"{i}. {item[0]} - {self.money(item[1])}")

    def output(self):
        print("\n" + "=" * 45)
        print("Траты за месяц")
        print("=" * 45)
        total = self.pref_sum[30]
        print(f"Итого потрачено: {self.money(total)}")
        print("\nТраты по дням:")
        empty = True
        for i in range(31):
            if self.days[i] != 0:
                print(f"День {i + 1:2d}: {self.money(self.days[i])}")
                empty = False
        if empty:
            print("Пока расходов нет")
        print("\nПрефиксные суммы:")
        print(self.pref_sum)
        print("\nКатегории:")
        if len(self.types_of_sp) == 0:
            print("Пока категорий нет.")
        else:
            for categ in self.types_of_sp:
                print(f"{categ}: {self.money(self.types_of_sp[categ])}")
        print("=" * 45 + "\n")

    def show_tree(self):
        print("\nДерево трат:")
        self.root.print_tree()
        print()


def read_int(text):
    while True:
        try:
            return int(input(text))
        except ValueError:
            print("Ошибка. Введите верное число")


def read_day(text):
    while True:
        day = read_int(text)
        if 1 <= day <= 31:
            return day
        else:
            print("Ошибка. Введите день от 1 до 31")


def read_amount(text):
    while True:
        try:
            value = int(input(text))
            if value <= 0:
                print("Сумма должна быть больше 0")
            else:
                return value
        except ValueError:
            print("Ошибка. Введите число")


def menu():
    ds = DailySpending()
    while True:
        print("\n" + "-" * 45)
        print("Бюджетный помощник")
        print("-" * 45)
        print("1. Добавить расход")
        print("2. Посчитать расходы за период")
        print("3. Найти день с максимальным расходом")
        print("4. Показать категории по сумме трат")
        print("5. Отменить последний расход")
        print("6. Показать все траты")
        print("7. Показать дерево трат")
        print("8. Выход")
        print("-" * 45)
        choice = input("Выберите действие: ")
        if choice == "1":
            day = read_day("Введите день месяца: ")
            amount = read_amount("Введите сумму расхода: ")
            categ = input("Введите категорию: ")
            ds.add_spending(amount, day, categ)
        elif choice == "2":
            day_A = read_day("Введите начальный день: ")
            day_B = read_day("Введите конечный день: ")
            ds.sum_from_to(day_A, day_B)
        elif choice == "3":
            ds.max_spending()
        elif choice == "4":
            ds.show_categories_sorted()
        elif choice == "5":
            ds.undo_last()
        elif choice == "6":
            ds.output()
        elif choice == "7":
            ds.show_tree()
        elif choice == "8":
            print("Всего доброго!")
            break
        else:
            print("Такого пункта в меню нет")


menu()
