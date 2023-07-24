from classes_bot import AddressBook, Name, Phone, Record, Birthday, BirthdayError, NameError
from sanitize import sanitize_phone_number
from datetime import datetime

address_book = AddressBook()


def input_error(func):
    def wrapper(*args):
        try:
            result = func(*args)
        except IndexError:
            return f"Введіть ім'я та номер контакту"
        return result
    return wrapper


def index_error(func):
    def wrapper(*args):
        try:
            result = func(*args)
        except IndexError:
            return f"Немає імені або номеру контакта"
        return result
    return wrapper


def key_error(func):
    def wrapper(*args):
        try:
            result = func(*args)
        except KeyError:
            return f"Контак {args[0].capitalize()} відсутній"
        return result
    return wrapper


@input_error
def add_command(*args):
    try:
        name = Name(args[0])
    except NameError as e:
        return e
    if len(args[1]) > 13 or len(args[1]) < 10:
        return f"Невірний формат номер телефона"
    phone = Phone(sanitize_phone_number(args[1]))
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.add_phone(phone)
    rec = Record(name, phone)
    return address_book.add_record(rec)


@key_error
def phone_print(*data):
    contact = data[0].capitalize().strip()
    result = address_book[contact]
    days_for_bd = days_to_bd(*data)
    return f"Контакт: {result} до дня народження {days_for_bd}"


@index_error
def change_command(*args):
    name = Name(args[0].capitalize())
    old_phone = Phone(sanitize_phone_number(args[1]))
    if len(args[2]) > 13 or len(args[2]) < 10:
        return f"Невірний формат номер телефона"
    new_phone = Phone(sanitize_phone_number(args[2]))
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.change_phone(old_phone, new_phone)
    return f"Немає {name} в списку кнтактів"


def hello_func(text=None):
    return f"Привіт, чим можу допомогти?"


def exit_command(*args):
    return "До побачення"


def unknown_command(*args):
    return f"Невідома команда"


def show_all_command(*args):
    for rec in address_book.iterator():
        print(rec)
        print("next page")
    return f"адресна книга надрукована"


def get_birth(*args):
    name = Name(args[0].capitalize())
    rec = address_book.get(str(name))
    if rec:
        try:
            birth = Birthday(args[1])
        except BirthdayError as e:
            return e
        return rec.add_birthday(birth)
    return f"Немає {name} в списку кнтактів"


def days_to_bd(*args):
    name = Name(args[0].capitalize())
    rec = address_book.get(str(name))
    if rec:
        return rec.days_for_birthday()
    return f"Немає {name} в списку контактів"

def search_in_adb(args):
    temp_result = []
    result = ''
    search = str(args)
    for key, val in address_book.items():
        if search in str(key.lower()) or search in str(val):
            temp_result.append(str(val))
    if len(temp_result) < 1:
        return f"{args} не знайдено"
    elif len(temp_result) == 1:
        return f"{temp_result[0]}"
    else:
       result = "\n".join(temp_result)
    return result


COMMANDS = {
    add_command: ("add", "+", "додати"),
    change_command: ("change", "зміни"),
    exit_command: ("до побачення", "до зустрічі", "exit", "by", "пока", "end"),
    show_all_command: ("show all", "показати все"),
    hello_func: ("hello", "hi", "привіт"),
    phone_print: ("phone", "друк", "print"),
    get_birth: ("birthday", "birth"),
    days_to_bd: ("days", "днюха"),
    search_in_adb: ("search", "пошук")
}


def parser(text: str):
    for cmd, kwds in COMMANDS.items():
        for kwd in kwds:
            if text.lower().startswith(kwd):
                data = text[len(kwd):].strip().split()
                return cmd, data
    return unknown_command, []


def main():
    while True:
        user_input = input(">>чекаю ввод>>")
        cmd, data = parser(user_input)
        result = cmd(*data)
        print(result)
        if cmd == exit_command:
            break


if __name__ == "__main__":
    main()
