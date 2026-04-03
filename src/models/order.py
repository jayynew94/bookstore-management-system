from dataclasses import dataclass, field
import uuid


@dataclass(frozen=True)
class Order:
    customer_id: str
    customer_name: str
    book_id: str
    book_title: str
    quantity: int
    total: float
    order_id: str = field(default_factory=lambda: uuid.uuid4().hex)

