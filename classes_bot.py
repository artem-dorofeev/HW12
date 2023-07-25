from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)


class NameError(Exception):
    ...


class Name(Field):
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value.capitalize()

    @value.setter
    def value(self, value):
        if len(value) < 2:
            raise NameError("Ім'я контакта має буди 2 або більше символів")
        self.__value = value


class PhoneError(Exception):
    ...


class Phone(Field):
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value.capitalize()

    @value.setter
    def value(self, value):
        new_phone = ''
        for i in value:
            if 48 <= ord(i) <= 57:
                new_phone += i
        if len(new_phone) < 7 or len(new_phone) > 12:
            raise PhoneError("Невірний формат номера")
        self.__value = new_phone



class BirthdayError(Exception):
    ...


class Birthday(Field):
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise BirthdayError("Дата повинна бути у форматі дд.мм.рррр")

    def __str__(self):
        return self.__value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None) -> None:
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday

    def add_phone(self, phone: Phone):
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return f"Телефон {phone} додано до контакту {self.name}"
        return f"{phone} вже є у контакта {self.name}"

    def change_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if old_phone.value == p.value:
                self.phones[idx] = new_phone
                return f"старий номер {old_phone} змінено на {new_phone}"
        return f"{old_phone} відсутній в списку контакта {self.name}"

    def add_birthday(self, birthday: Birthday):
        self.birthday = birthday
        return f"{birthday} add to {self.name}"

    def days_for_birthday(self):
        if not self.birthday:
            return f"відсутня дата народження {self.name}"
        birth = self.birthday.value
        current_date = datetime.now()
        next_birth = datetime(current_date.year, birth.month, birth.day)
        if next_birth < current_date:
            next_birth = datetime(current_date.year + 1,
                                  birth.month, birth.day)
        day_for_birth = next_birth - current_date
        return day_for_birth.days

    def __str__(self) -> str:
        return f"{self.name}: {', '.join(str(p) for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return f"Контакт {record} додано успішно"

    def iterator(self, n=3):
        result = ''
        count = 0
        for cont in self.values():
            result += str(cont) + "\n"
            count += 1
            if count >= n:
                yield result
                count = 0
                result = ""
        if result:
            yield result

    def __getitem__(self, key):
        return super().__getitem__(key)

    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())
