from ..bl.library import Library
from .exceptions import *


def show_commands() -> None:
    """Вывод всех возможный действий в терминале"""
    print("\nМеню (введите цифру от 1 до 6):")
    print('"1" - Добавить книгу')
    print('"2" - Удалить книгу')
    print('"3" - Найти книгу')
    print('"4" - Показать все книги')
    print('"5" - Изменить статус книги')
    print('"6" - Выйти')


def process_terminal_commands(library: Library) -> None:
    """Обработка команд пользователя"""
    choice = input("\nВыберите действие: ")

    if choice == "1":
        title = input("Введите название книги: ")
        author = input("Введите автора книги: ")
        try:
            year = year_not_int_exception("Введите год издания: ")
            library.add_book(title, author, year)
        except Exception as e:
            print(f"{e}")

    elif choice == "2":
        try:
            book_id = id_not_int_exception("Введите ID книги для удаления: ")
            library.remove_book(book_id)
        except Exception as e:
            print(f"{e}")

    elif choice == "3":
        field = input("Введите поле для поиска (title, author, year): ")
        if field in ["title", "author", "year"]:
            query = input("Введите запрос для поиска: ")
            results = library.search_books(query, field)
            if results:
                print("\nНайденные книги:")
                for book in results:
                    print(Library.format_book(book))
            else:
                print("\nКниги не найдены.\n")
        else:
            print("\nНедопустимое поле. Доступны: title, author, year.\n")

    elif choice == "4":
        result = library.list_books()
        if not result:
            print("\nБиблиотека пуста.\n")
        else:
            print("\nСписок книг:")
            for book in result:
                print(Library.format_book(book))

    elif choice == "5":
        try:
            book_id = id_not_int_exception("Введите ID книги для изменения статуса: ")
            status = input("Введите новый статус ('в наличии' или 'выдана'): ")
            library.update_status(book_id, status)
        except Exception as e:
            print(f"{e}")

    elif choice == "6":
        print("\nВыход из программы.")
        exit()

    else:
        print("\nНедопустимый выбор. Выберите число от 1 до 6 (около числа не должно быть пробелов).\n")
