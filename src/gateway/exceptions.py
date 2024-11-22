def year_not_int_exception(message: str) -> int:
    """Исключение в случае ввода не типа int, когда он необходим"""
    try:
        result = int(input(message))
        return result
    except ValueError:
        raise ValueError("\nГод должен быть числом!\n")


def id_not_int_exception(message: str) -> int:
    """Исключение в случае ввода не типа int, когда он необходим"""
    try:
        result = int(input(message))
        return result
    except ValueError:
        raise ValueError("\nID должен быть числом!\n")
