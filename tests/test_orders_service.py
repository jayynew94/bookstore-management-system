import unittest

from models import Book
from services.inventory_service import InventoryService
from services.orders_service import OrdersService


class OrdersServiceTests(unittest.TestCase):
    def setUp(self):
        self.book = Book("Dune", "Frank Herbert", "Science Fiction", 14.5, 8)
        self.inventory_service = InventoryService([self.book])
        self.orders_service = OrdersService(self.inventory_service, customers=[], orders=[])

    def test_add_customer_requires_valid_email(self):
        with self.assertRaisesRegex(ValueError, "valid email"):
            self.orders_service.add_customer("Casey", "bad-email")

    def test_place_order_reduces_stock_and_records_order(self):
        customer = self.orders_service.add_customer("Casey", "casey@example.com")

        order = self.orders_service.place_order(customer.customer_id, self.book.book_id, 2)

        self.assertEqual(order.total, 29.0)
        self.assertEqual(order.status, "Completed")
        self.assertEqual(self.orders_service.total_orders(), 1)
        self.assertEqual(self.inventory_service.get_book(self.book.book_id).quantity, 6)

    def test_place_order_invalid_quantity(self):
        customer = self.orders_service.add_customer("Casey", "casey@example.com")

        with self.assertRaises(ValueError):
            self.orders_service.place_order(customer.customer_id, self.book.book_id, 0)

    def test_place_order_invalid_customer(self):
        with self.assertRaises(ValueError):
            self.orders_service.place_order("bad-id", self.book.book_id, 1)

    def test_filter_orders_by_customer_and_date(self):
        customer = self.orders_service.add_customer("Casey", "casey@example.com")
        second_customer = self.orders_service.add_customer("Jordan", "jordan@example.com")
        self.orders_service.place_order(customer.customer_id, self.book.book_id, 1, status="Submitted")
        self.orders_service.place_order(second_customer.customer_id, self.book.book_id, 1, status="Completed")

        results = self.orders_service.filter_orders(
            start_date="2000-01-01",
            end_date="2100-01-01",
            customer_id=customer.customer_id,
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].customer_name, "Casey")

    def test_ensure_customer_reuses_existing_customer(self):
        existing = self.orders_service.add_customer("Casey", "casey@example.com")

        ensured = self.orders_service.ensure_customer("Casey", "casey@example.com")

        self.assertEqual(existing.customer_id, ensured.customer_id)


if __name__ == "__main__":
    unittest.main()
