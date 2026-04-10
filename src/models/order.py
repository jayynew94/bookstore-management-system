from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass(frozen=True)
class Order:
    customer_id: str
    customer_name: str
    book_id: str
    book_title: str
    quantity: int
    total: float
    status: str = "Completed"
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    order_id: str = field(default_factory=lambda: uuid.uuid4().hex)
