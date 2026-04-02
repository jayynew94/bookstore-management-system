import tempfile
import unittest
from pathlib import Path

from models import Book, Customer, Order
from services.data_store import JsonDataStore


class JsonDataStoreTests(unittest.TestCase):
    def test_save_and_load_round_trip(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "bookstore_data.json"
            store = JsonDataStore(path)

            books = [Book("Dune", "Frank Herbert", "Science Fiction", 14.5, 8, "book-1")]
            customers = [Customer("Casey", "casey@example.com", "customer-1")]
            orders = [
                Order(
                    "customer-1",
                    "Casey",
                    "book-1",
                    "Dune",
                    2,
                    29.0,
                    "order-1",
                )
            ]

            store.save(books, customers, orders)
            loaded = store.load()

            self.assertTrue(store.exists())
            self.assertEqual(loaded["books"][0]["book_id"], "book-1")
            self.assertEqual(loaded["customers"][0]["customer_id"], "customer-1")
            self.assertEqual(loaded["orders"][0]["order_id"], "order-1")


if __name__ == "__main__":
    unittest.main()
