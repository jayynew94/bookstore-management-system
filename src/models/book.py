from dataclasses import dataclass, field
import uuid


@dataclass
class Book:
    """
    Represents a book in the inventory.
    """
    title: str
    author: str
    genre: str
    price: float
    quantity: int
    book_id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __str__(self):
        """
        Defines how the book appears when printed.
        """
        return (
            f"{self.book_id} | {self.title} | {self.author} | "
            f"{self.genre} | ${self.price:.2f} | Stock: {self.quantity}"
        )