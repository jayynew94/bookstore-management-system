import tkinter as tk
from tkinter import messagebox
from pathlib import Path

from models import Book, Customer, Order
from services import AuthService, InventoryService, JsonDataStore, OrdersService
from ui.customer_window import CustomerWindow
from ui.dashboard_window import DashboardWindow
from ui.inventory_window import InventoryWindow
from ui.login_window import LoginWindow
from ui.orders_window import OrdersWindow


class BookstoreApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Bookstore Management System")
        self.root.geometry("860x620")
        self.root.minsize(760, 560)

        self.auth_service = AuthService()
        data_path = Path(__file__).resolve().parent.parent / "data" / "bookstore_data.json"
        self.data_store = JsonDataStore(data_path)
        data = self.data_store.load()

        books = [Book(**book) for book in data["books"]] if self.data_store.exists() else None
        customers = [Customer(**customer) for customer in data["customers"]]
        orders = [Order(**order) for order in data["orders"]]

        self.inventory_service = InventoryService(books, save_callback=self.save_data)
        self.orders_service = OrdersService(
            self.inventory_service,
            customers=customers,
            orders=orders,
            save_callback=self.save_data,
        )
        self.current_frame = None
        self.username = ""
        self.current_role = ""

        self.save_data()
        self.show_login()

    def _swap_frame(self, frame_class, *args):
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = frame_class(self.root, *args)
        self.current_frame.pack(fill="both", expand=True)

    def show_login(self):
        self.username = ""
        self.current_role = ""
        self._swap_frame(LoginWindow, self.auth_service, self.handle_login_success)

    def handle_login_success(self, user: dict):
        self.username = user["display_name"]
        self.current_role = user["role"]
        if self.current_role == "staff":
            self.show_dashboard()
            return
        self.show_customer_view()

    def show_dashboard(self):
        self._swap_frame(
            DashboardWindow,
            self.username,
            self.inventory_service,
            self.show_inventory,
            self.orders_service,
            self.show_orders,
            self.show_login,
        )

    def show_inventory(self):
        if self.current_role != "staff":
            messagebox.showerror("Access Denied", "Only staff users can access inventory management.")
            self.show_customer_view()
            return
        self._swap_frame(InventoryWindow, self.inventory_service, self.show_dashboard)

    def show_orders(self):
        if self.current_role != "staff":
            messagebox.showerror("Access Denied", "Only staff users can access staff order management.")
            self.show_customer_view()
            return
        self._swap_frame(
            OrdersWindow,
            self.inventory_service,
            self.orders_service,
            self.show_dashboard,
        )

    def show_customer_view(self):
        self._swap_frame(
            CustomerWindow,
            self.username,
            self.inventory_service,
            self.show_login,
        )

    def save_data(self):
        self.data_store.save(
            self.inventory_service.list_books(),
            self.orders_service.list_customers(),
            self.orders_service.list_orders(),
        )
