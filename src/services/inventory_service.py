from __future__ import annotations

from dataclasses import replace

from models import Book


class InventoryService:
    def __init__(self, books: list[Book] | None = None, save_callback=None):
        self._books = books[:] if books is not None else self._default_books()
        self._save_callback = save_callback

    def list_books(self) -> list[Book]:
        return sorted(self._books, key=lambda book: book.title.lower())

    def get_book(self, book_id: str) -> Book:
        for book in self._books:
            if book.book_id == book_id:
                return book
        raise ValueError("Selected book could not be found.")

    def add_book(
        self,
        title: str,
        author: str,
        genre: str,
        price: float,
        quantity: int,
    ) -> Book:
        title = title.strip()
        author = author.strip()
        genre = genre.strip()

        if not title or not author or not genre:
            raise ValueError("Title, author, and genre are required.")

        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        book = Book(
            title=title,
            author=author,
            genre=genre,
            price=round(price, 2),
            quantity=quantity,
        )
        self._books.append(book)
        self._persist()
        return book

    def update_book(
        self,
        book_id: str,
        title: str,
        author: str,
        genre: str,
        price: float,
        quantity: int,
    ) -> Book:
        book = self.get_book(book_id)
        updated_book = replace(
            book,
            title=title.strip(),
            author=author.strip(),
            genre=genre.strip(),
            price=round(price, 2),
            quantity=quantity,
        )
        self._validate(updated_book)
        self._replace_book(updated_book)
        self._persist()
        return updated_book

    def delete_book(self, book_id: str):
        book = self.get_book(book_id)
        self._books.remove(book)
        self._persist()

    def reduce_stock(self, book_id: str, quantity: int):
        book = self.get_book(book_id)
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")
        if book.quantity < quantity:
            raise ValueError("Not enough stock is available for this order.")

        updated_book = replace(book, quantity=book.quantity - quantity)
        self._replace_book(updated_book)
        self._persist()
        return updated_book

    def total_titles(self) -> int:
        return len(self._books)

    def total_stock(self) -> int:
        return sum(book.quantity for book in self._books)

    def inventory_value(self) -> float:
        return round(sum(book.price * book.quantity for book in self._books), 2)

    def _replace_book(self, updated_book: Book):
        for index, book in enumerate(self._books):
            if book.book_id == updated_book.book_id:
                self._books[index] = updated_book
                return
        raise ValueError("Selected book could not be found.")

    def _validate(self, book: Book):
        if not book.title or not book.author or not book.genre:
            raise ValueError("Title, author, and genre are required.")
        if book.price <= 0:
            raise ValueError("Price must be greater than 0.")
        if book.quantity < 0:
            raise ValueError("Quantity cannot be negative.")

    def _persist(self):
        if self._save_callback is not None:
            self._save_callback()

    @staticmethod
    def _default_books() -> list[Book]:
        return [
            Book("Atomic Habits", "James Clear", "Self-Help", 18.99, 12),
            Book("Dune", "Frank Herbert", "Science Fiction", 14.50, 8),
            Book("The Hobbit", "J.R.R. Tolkien", "Fantasy", 13.25, 10),
            Book("The Martian", "Andy Weir", "Science Fiction", 16.75, 6),
        ]
