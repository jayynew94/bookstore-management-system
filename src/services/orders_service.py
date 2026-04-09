from __future__ import annotations

from models import Customer, Order


class OrdersService:
    def __init__(
        self,
        inventory_service,
        customers: list[Customer] | None = None,
        orders: list[Order] | None = None,
        save_callback=None,
    ):
        self.inventory_service = inventory_service
        self._customers = customers[:] if customers is not None else []
        self._orders = orders[:] if orders is not None else []
        self._save_callback = save_callback

    def list_customers(self) -> list[Customer]:
        return sorted(self._customers, key=lambda customer: customer.name.lower())

    def list_orders(self) -> list[Order]:
        return self._orders[:]

    def get_order(self, order_id: str) -> Order:
        for order in self._orders:
            if order.order_id == order_id:
                return order
        raise ValueError("Selected order could not be found.")

    def add_customer(self, name: str, email: str) -> Customer:
        name = name.strip()
        email = email.strip().lower()

        if not name or not email:
            raise ValueError("Customer name and email are required.")

        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("Please enter a valid email address.")

        customer = Customer(name=name, email=email)
        self._customers.append(customer)
        self._persist()
        return customer

    def ensure_customer(self, name: str, email: str) -> Customer:
        email = email.strip().lower()
        for customer in self._customers:
            if customer.email == email:
                return customer
        return self.add_customer(name, email)

    def place_order(
        self,
        customer_id: str,
        book_id: str,
        quantity: int,
        status: str = "Completed",
    ) -> Order:
        if quantity <= 0:
            raise ValueError("Order quantity must be greater than 0.")

        customer = self.get_customer(customer_id)
        book = self.inventory_service.get_book(book_id)
        updated_book = self.inventory_service.reduce_stock(book_id, quantity)

        order = Order(
            customer_id=customer.customer_id,
            customer_name=customer.name,
            book_id=updated_book.book_id,
            book_title=updated_book.title,
            quantity=quantity,
            total=round(book.price * quantity, 2),
            status=status,
        )
        self._orders.append(order)
        self._persist()
        return order

    def get_customer(self, customer_id: str) -> Customer:
        for customer in self._customers:
            if customer.customer_id == customer_id:
                return customer
        raise ValueError("Selected customer could not be found.")

    def total_orders(self) -> int:
        return len(self._orders)

    def total_revenue(self) -> float:
        return round(sum(order.total for order in self._orders), 2)

    def filter_orders(
        self,
        start_date: str = "",
        end_date: str = "",
        customer_id: str = "",
    ) -> list[Order]:
        orders = self._orders[:]

        if customer_id:
            orders = [order for order in orders if order.customer_id == customer_id]

        if start_date:
            orders = [order for order in orders if order.created_at >= start_date]

        if end_date:
            orders = [order for order in orders if order.created_at <= end_date]

        return orders

    def _persist(self):
        if self._save_callback is not None:
            self._save_callback()
