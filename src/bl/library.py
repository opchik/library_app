import json
from datetime import datetime
from typing import List, Dict, Union

from .book import Book
from ..config import LIBRARY_FILENAME


CURRENT_YEAR = datetime.now().year


class Library:
    """Класс для управления библиотекой"""

    def __init__(self, filename: str = LIBRARY_FILENAME):
        self.filename = filename
        self.books: List[Book] = []
        self.load_books()

    def load_books(self) -> None:
        """Загрузка книги из файла"""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.books = [Book.from_dict(book) for book in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.books = []

    def save_books(self) -> None:
        """Сохранение книги в файл"""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(
                [book.to_dict() for book in self.books],
                file,
                ensure_ascii=False,
                indent=4,
            )

    def add_book(self, title: str, author: str, year: int) -> None:
        """Добавление книги в библиотеку"""

        if title == "" or author == "" or year > CURRENT_YEAR:
            raise ValueError("Заполните все данные или введите корректный год.")
        new_id = max((book.id for book in self.books), default=0) + 1
        new_book = Book(new_id, title, author, year)
        self.books.append(new_book)
        self.save_books()
        print(f"\nКнига '{title}' добавлена с ID {new_id}.\n")

    def remove_book(self, book_id: int) -> None:
        """Удаление книги из библиотеки"""
        book = next((book for book in self.books if book.id == book_id), None)
        if book:
            self.books.remove(book)
            self.save_books()
            print(f"\nКнига с ID {book_id} удалена.\n")
        else:
            raise ValueError(f"\nКнига с ID {book_id} не найдена.\n")

    def search_books(self, query: str, field: str) -> List[Book]:
        """Поиск книги по указанному полю"""
        results = [
            book
            for book in self.books
            if query.lower() in str(getattr(book, field)).lower()
        ]
        return results

    def list_books(self) -> List[Book]:
        """Вывод списка всех книг"""
        return self.books

    def update_status(self, book_id: int, status: str) -> None:
        """Обновление статуса книги"""
        book = next((book for book in self.books if book.id == book_id), None)
        if book:
            if status in ["в наличии", "выдана"]:
                book.status = status
                self.save_books()
                print(f"\nСтатус книги с ID {book_id} обновлен на '{status}'.")
            else:
                raise ValueError("\nНеверный статус. Введите 'в наличии' или 'выдана'.\n")
        else:
            raise ValueError(f"\nКнига с ID {book_id} не найдена.\n")

    @staticmethod
    def format_book(book: Book) -> str:
        """Форматирование информации о книге для отображения"""
        return f"ID: {book.id}, Название: '{book.title}', Автор: {book.author}, Год: {book.year}, Статус: {book.status}"
