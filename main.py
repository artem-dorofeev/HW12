from classes_bot import AddressBook, Name, Phone, Record, Birthday, BirthdayError, NameError, PhoneError
from datetime import datetime
import pickle

address_book = AddressBook()


def file_error(func):
    def wrapper():
        try:
            result = func()
        except FileNotFoundError:
            address_book = AddressBook()
            return f"Немає доступу до файла, створена нова адресна книга"
        return result
    return wrapper


# @file_error
# def load_adb_from_file():
#     global address_book
#     with open("adr_book.bin", "rb") as f:
#         address_book = pickle.load(f)
#     return f"Адресна книга загружена з файлу"

@file_error
def load_adb_from_file():
    # global address_book
    AddressBook.load_adb_from_file(address_book)
    return f"load OK"


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
            return f"Немає імені або номеру або дати народження контакта"
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
    try:
        phone = Phone(args[1])
    except PhoneError as f:
        return f
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
    return f"Контакт: {result} до дня народження {days_for_bd} днів"


@index_error
def change_command(*args):
    name = Name(args[0].capitalize())
    try:
        old_phone = Phone(args[1])
    except PhoneError as f:
        return f
    try:
        new_phone = Phone(args[2])
    except PhoneError as f:
        return f
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


@index_error
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


# def search_in_adb(args):
#     temp_result = []
#     result = ''
#     search = str(args)
#     for key, val in address_book.items():
#         if search in str(key.lower()) or search in str(val):
#             temp_result.append(str(val))
#     if len(temp_result) < 1:
#         return f"{args} не знайдено"
#     elif len(temp_result) == 1:
#         return f"{temp_result[0]}"
#     else:
#         result = "\n".join(temp_result)
#     return result

def search_in_adb(args):
    result = AddressBook.search_cont(address_book, args)
    return result


def write_adb_to_file():
    # file_name = "adr_book.bin"
    result = AddressBook.write_adb_to_file(address_book)
    # with open(file_name, "wb") as f:
    #     pickle.dump(address_book, f)
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
    search_in_adb: ("search", "пошук"),
    write_adb_to_file: ("backup", "резервування", "копія")
}


def parser(text: str):
    for cmd, kwds in COMMANDS.items():
        for kwd in kwds:
            if text.lower().startswith(kwd):
                data = text[len(kwd):].strip().split()
                return cmd, data
    return unknown_command, []


def main():

    load_adb = load_adb_from_file()
    print(load_adb)

    while True:
        user_input = input(">>чекаю ввод>>")
        cmd, data = parser(user_input)
        result = cmd(*data)
        print(result)
        if cmd == add_command or cmd == change_command or cmd == get_birth:
            backup = AddressBook.write_adb_to_file(address_book)
            print(backup)
        if cmd == exit_command:
            break


if __name__ == "__main__":
    main()
