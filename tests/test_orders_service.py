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
        self.assertEqual(self.orders_service.total_orders(), 1)
        self.assertEqual(self.inventory_service.get_book(self.book.book_id).quantity, 6)


if __name__ == "__main__":
    unittest.main()

