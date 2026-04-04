import unittest

from models import Book
from services.inventory_service import InventoryService


class InventoryServiceTests(unittest.TestCase):
    def test_lists_books_sorted_by_title(self):
        service = InventoryService(
            [
                Book("Zulu", "A", "Fiction", 10.0, 1),
                Book("alpha", "B", "Fiction", 11.0, 1),
            ]
        )

        titles = [book.title for book in service.list_books()]
        self.assertEqual(titles, ["alpha", "Zulu"])

    def test_add_book_updates_inventory_totals(self):
        service = InventoryService([])

        service.add_book("Clean Code", "Robert C. Martin", "Software", 30.0, 4)

        self.assertEqual(service.total_titles(), 1)
        self.assertEqual(service.total_stock(), 4)
        self.assertEqual(service.inventory_value(), 120.0)

    def test_add_book_rejects_invalid_data(self):
        service = InventoryService([])

        with self.assertRaisesRegex(ValueError, "required"):
            service.add_book("", "Author", "Genre", 10, 1)

        with self.assertRaisesRegex(ValueError, "greater than 0"):
            service.add_book("Title", "Author", "Genre", 0, 1)

        with self.assertRaisesRegex(ValueError, "cannot be negative"):
            service.add_book("Title", "Author", "Genre", 10, -1)

    def test_update_book_changes_existing_record(self):
        original = Book("Dune", "Frank Herbert", "Science Fiction", 14.5, 8)
        service = InventoryService([original])

        updated = service.update_book(
            original.book_id,
            "Dune Messiah",
            "Frank Herbert",
            "Science Fiction",
            15.0,
            7,
        )

        self.assertEqual(updated.title, "Dune Messiah")
        self.assertEqual(service.get_book(original.book_id).quantity, 7)

    def test_delete_book_removes_record(self):
        book = Book("Dune", "Frank Herbert", "Science Fiction", 14.5, 8)
        service = InventoryService([book])

        service.delete_book(book.book_id)

        self.assertEqual(service.total_titles(), 0)

    def test_reduce_stock_rejects_oversell(self):
        book = Book("Dune", "Frank Herbert", "Science Fiction", 14.5, 2)
        service = InventoryService([book])

        with self.assertRaisesRegex(ValueError, "Not enough stock"):
            service.reduce_stock(book.book_id, 3)

    def test_get_book_returns_single_record_details(self):
        book = Book("Dune", "Frank Herbert", "Science Fiction", 14.5, 2)
        service = InventoryService([book])

        selected = service.get_book(book.book_id)

        self.assertEqual(selected.title, "Dune")
        self.assertEqual(selected.author, "Frank Herbert")


if __name__ == "__main__":
    unittest.main()
