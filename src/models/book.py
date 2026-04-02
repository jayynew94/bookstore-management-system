from dataclasses import dataclass, field
import uuid


@dataclass(frozen=True)
class Book:
    title: str
    author: str
    genre: str
    price: float
    quantity: int
    book_id: str = field(default_factory=lambda: uuid.uuid4().hex)
