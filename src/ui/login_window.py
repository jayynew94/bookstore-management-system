import tkinter as tk
from tkinter import messagebox

from models.book import Book
from services.book_service import BookService
from ui.inventory_window import InventoryWindow


USERS = {
    "admin": {"password": "admin123", "role": "Admin"},
    "staff": {"password": "staff123", "role": "Staff"},
    "customer": {"password": "cust123", "role": "Customer"},
}


class LoginApp:
    """
    Creates the login window for the bookstore system.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Book Management System - Login")
        self.root.geometry("420x260")

        tk.Label(self.root, text="Login", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        self.username = tk.Entry(self.root)
        self.username.pack()

        tk.Label(self.root, text="Password").pack()
        self.password = tk.Entry(self.root, show="*")
        self.password.pack()

        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)

        tk.Label(
            self.root,
            text="Demo logins: admin/admin123, staff/staff123, customer/cust123",
            wraplength=350,
            justify="center"
        ).pack(pady=10)

    def login(self):
        """
        Validate credentials and open the next screen.
        """
        username = self.username.get().strip()
        password = self.password.get().strip()

        if not username:
            messagebox.showwarning("Error", "Username is required")
            return

        if not password:
            messagebox.showwarning("Error", "Password is required")
            return

        if username not in USERS or USERS[username]["password"] != password:
            messagebox.showerror("Error", "Invalid credentials")
            return

        role = USERS[username]["role"]
        messagebox.showinfo("Success", f"Welcome {username} ({role})")

        if role in ["Admin", "Staff"]:
            self.open_inventory_window()
        else:
            self.open_customer_dashboard(username)

    def open_inventory_window(self):
        """
        Replace the login UI with the inventory UI.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

        inventory_service = BookService()

        inventory_service.add_book(Book("Python Basics", "John Smith", "Programming", 29.99, 10))
        inventory_service.add_book(Book("Advanced Python Programming", "Jane Doe", "Programming", 39.99, 5))
        inventory_service.add_book(Book("Database Systems", "Mike Brown", "Technology", 45.50, 8))
        inventory_service.add_book(Book("Bookstore Operations", "Sarah Green", "Business", 22.75, 12))

        inventory_window = InventoryWindow(
            self.root,
            inventory_service,
            self.show_login_screen
        )
        inventory_window.pack(fill="both", expand=True)

    def show_login_screen(self):
        """
        Return to the login screen.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

        login_app = LoginApp(self.root)

    def open_customer_dashboard(self, username):
        """
        Open a simple customer dashboard.
        """
        dashboard = tk.Toplevel(self.root)
        dashboard.title("Customer Dashboard")
        dashboard.geometry("350x180")

        tk.Label(
            dashboard,
            text=f"Welcome, {username}",
            font=("Arial", 14, "bold")
        ).pack(pady=15)

        tk.Label(
            dashboard,
            text="Customers can browse books and manage purchases.",
            wraplength=280,
            justify="center"
        ).pack(pady=10)