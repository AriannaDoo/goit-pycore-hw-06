from collections import UserDict


class Field:
    """
    Базовий клас для полів запису (ім'я, телефон)
    Зберігає тільки значення у атрибуті value
    """

    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """
    Клас для зберігання імені контакту
    Успадковується від Field
    """
    pass


class Phone(Field):
    """
    Клас для зберігання номера телефону
    Додає просту валідацію - номер має складатися тільки з цифр та містити 10 символів
    """

    def __init__(self, value: str) -> None:
        if not self._is_valid(value):
            raise ValueError("Невірний формат номера телефону. Очікується 10 цифр.")
        super().__init__(value)

    @staticmethod
    def _is_valid(value: str) -> bool:
        """Перевіряє, що номер складається лише з цифр та має довжину 10 символів."""
        return value.isdigit() and len(value) == 10


class Record:
    """
    Клас для зберігання інформації про контакт:
    - обов'язкове поле name (типу Name)
    - список телефонів phones (список об'єктів Phone)
    """

    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones: list[Phone] = []

    def add_phone(self, phone: str) -> None:
        """
        Додає новий номер телефону до контакту.
        Приймає рядок, всередині створюється об'єкт Phone з валідацією.
        """
        self.phones.append(Phone(phone))

    def find_phone(self, phone: str) -> Phone | None:
        """
        Шукає телефон у списку phones за значенням
        Повертає об'єкт Phone або None якщо номер не знайдено
        """
        for ph in self.phones:
            if ph.value == phone:
                return ph
        return None

    def remove_phone(self, phone: str) -> None:
        """
        Видаляє номер телефону з запису якщо він існує
        Нічого не робить якщо номер не знайдено
        """
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """
        Замінює існуючий номер телефону - на новий
        Якщо старий номер не знайдено — піднімає ValueError
        """
        phone_obj = self.find_phone(old_phone)
        if not phone_obj:
            raise ValueError(f"Номер {old_phone} не знайдено у контакті {self.name.value}.")

        # Створюємо новий об'єкт Phone (тут може вилетіти ValueError, якщо формат некоректний)
        new_phone_obj = Phone(new_phone)

        # Замінюємо об'єкт у списку
        index = self.phones.index(phone_obj)
        self.phones[index] = new_phone_obj

    def __str__(self) -> str:
        """
        Рядкове представлення запису
        """
        phones_str = "; ".join(phone.value for phone in self.phones) if self.phones else "немає номерів"
        return f"Contact name: {self.name.value}, phones: {phones_str}"


class AddressBook(UserDict):
    """
    Клас адресної книги
    """

    def add_record(self, record: Record) -> None:
        """
        Додає запис (Record) до адресної книги
        Ключем виступає значення імені контакту
        """
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        """
        Пошук запису за ім'ям
        Повертає Record або None, якщо контакт не знайдено
        """
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """
        Видаляє запис за ім'ям з адресної книги
        Якщо імені немає - нічого не робить
        """
        if name in self.data:
            del self.data[name]
            
# Тестуємо реалізацію за допомогою прикладу з завдання     
if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону в записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
