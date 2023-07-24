def format_phone_number(func):
    def wrapper(x):
        result = func(x)
        if len(result) == 12:
            result = '+' + result
        elif len(result) == 11:
            result = '+3' + result
        else:
            result = '+38' + result
        return result
    return wrapper


@format_phone_number
def sanitize_phone_number(phone):
    new_phone = (
        phone.strip()
        .removeprefix("+")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "")
        .replace(" ", "")
    )
    return new_phone


if __name__ == "__main__":
    sanitize_phone_number()