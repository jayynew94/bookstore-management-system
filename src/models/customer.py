from dataclasses import dataclass, field
import uuid


@dataclass(frozen=True)
class Customer:
    name: str
    email: str
    customer_id: str = field(default_factory=lambda: uuid.uuid4().hex)

