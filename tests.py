import os
import unittest

from src.bl.book import Book
from src.bl.library import Library


class TestLibrary(unittest.TestCase):
    def setUp(self):
        """Создание тестовой библиотеки и временного файла для тестов."""
        self.test_file = "test_library.json"
        self.library = Library(self.test_file)
        self.library.books = [
            Book(1, "1984", "George Orwell", 1949, "в наличии"),
            Book(2, "Brave New World", "Aldous Huxley", 1932, "выдана"),
        ]
        self.library.save_books()

    def tearDown(self):
        """Удаление временного файла после завершения тестов."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    # Основные тесты
    def test_add_book(self):
        """Тест добавления книги."""
        self.library.add_book("Fahrenheit 451", "Ray Bradbury", 1953)
        self.assertEqual(len(self.library.books), 3)
        self.assertEqual(self.library.books[-1].title, "Fahrenheit 451")
        self.assertEqual(self.library.books[-1].status, "в наличии")

    def test_remove_book(self):
        """Тест удаления книги."""
        self.library.remove_book(1)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].id, 2)

        # Попытка удалить несуществующую книгу
        with self.assertRaises(ValueError):
            self.library.remove_book(99)

    def test_search_books_by_title(self):
        """Тест поиска книг по названию."""
        results = [book.title for book in self.library.books if "1984" in book.title]
        self.assertIn("1984", results)

    def test_update_status(self):
        """Тест изменения статуса книги."""
        self.library.update_status(1, "выдана")
        self.assertEqual(self.library.books[0].status, "выдана")

        # Попытка изменить статус несуществующей книги
        with self.assertRaises(ValueError):
            self.library.update_status(99, "в наличии")

    # Тесты для обработки ошибок
    def test_add_book_with_empty_fields(self):
        """Тест добавления книги с пустыми полями."""
        with self.assertRaises(ValueError):
            self.library.add_book("", "Unknown", 2000)
        with self.assertRaises(ValueError):
            self.library.add_book("Some Title", "", 2000)

    def test_remove_book_invalid_id(self):
        """Тест удаления книги с некорректным ID."""
        with self.assertRaises(ValueError):
            self.library.remove_book("abc")
        with self.assertRaises(ValueError):
            self.library.remove_book(-1)

    def test_update_status_invalid_status(self):
        """Тест изменения статуса книги с некорректным значением."""
        with self.assertRaises(ValueError):
            self.library.update_status(1, "неизвестный статус")

    # Граничные случаи
    def test_search_empty_library(self):
        """Тест поиска в пустой библиотеке."""
        self.library.books = []
        self.library.save_books()
        results = self.library.search_books("1984", "title")
        self.assertEqual(len(results), 0)

    def test_large_year_value(self):
        """Тест обработки некорректного года издания."""
        with self.assertRaises(ValueError):
            self.library.add_book("Future Book", "Author", 3000)

    def test_save_and_load_consistency(self):
        """Тест корректности сохранения и загрузки."""
        self.library.add_book("Test Book", "Test Author", 2024)
        self.library.save_books()

        # Проверяем загрузку из файла
        new_library = Library(self.test_file)
        self.assertEqual(len(new_library.books), 3)
        self.assertEqual(new_library.books[-1].title, "Test Book")


if __name__ == "__main__":
    unittest.main()
