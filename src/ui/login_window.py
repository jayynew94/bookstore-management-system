import tkinter as tk
from tkinter import messagebox

from services.auth_service import AuthService
from services.inventory_service import InventoryService
from ui.inventory_window import InventoryWindow


class LoginApp:
    """
    Creates the login window for the bookstore system.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Book Management System - Login")
        self.root.geometry("420x260")
        self.auth_service = AuthService()
        # Keep one shared inventory service for the session so admin/staff CRUD
        # actions are working against the same in-memory catalog after login.
        self.inventory_service = InventoryService()

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
            text="Demo logins: admin/admin123, staff1/books123, customer1/reader123",
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

        is_valid, message, user = self.auth_service.authenticate(username, password)
        if not is_valid:
            messagebox.showerror("Error", message)
            return

        role = user["role"]
        display_name = user["display_name"]
        messagebox.showinfo("Success", f"Welcome {display_name} ({role.title()})")

        # Admin and staff share the same catalog management permissions. This is
        # the role gate that controls who can add, edit, and delete books.
        if self._can_manage_books(role):
            self.open_inventory_window()
        else:
            self.open_customer_dashboard(display_name)

    @staticmethod
    def _can_manage_books(role):
        return role in {"admin", "staff"}

    def open_inventory_window(self):
        """
        Replace the login UI with the inventory UI.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

        inventory_window = InventoryWindow(
            self.root,
            self.inventory_service,
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
