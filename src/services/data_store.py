from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from models import Book, Customer, Order


class JsonDataStore:
    def __init__(self, path: Path):
        self.path = path

    def exists(self) -> bool:
        return self.path.exists()

    def load(self) -> dict[str, list[dict]]:
        if not self.path.exists():
            return {"books": [], "customers": [], "orders": []}

        with self.path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return {
            "books": data.get("books", []),
            "customers": data.get("customers", []),
            "orders": data.get("orders", []),
        }

    def save(self, books: list[Book], customers: list[Customer], orders: list[Order]):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "books": [asdict(book) for book in books],
            "customers": [asdict(customer) for customer in customers],
            "orders": [asdict(order) for order in orders],
        }
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2)

