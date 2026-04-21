import tkinter as tk
from tkinter import messagebox

from services.auth_service import AuthService
from services.inventory_service import InventoryService
from services.orders_service import OrdersService
from ui.customer_window import CustomerWindow
from ui.inventory_window import InventoryWindow


class LoginApp:
    """
    Creates the login window for the bookstore system.
    """

    def __init__(self, root, inventory_service=None, orders_service=None, auth_service=None):
        self.root = root
        self.root.title("Book Management System - Login")
        self.root.geometry("420x260")
        self.auth_service = auth_service or AuthService()
        # Keep one shared inventory service for the session so admin/staff CRUD
        # actions are working against the same in-memory catalog after login.
        self.inventory_service = inventory_service or InventoryService()
        self.orders_service = orders_service or OrdersService(self.inventory_service)

        tk.Label(self.root, text="Login", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        self.username = tk.Entry(self.root)
        self.username.pack()

        tk.Label(self.root, text="Password").pack()
        self.password = tk.Entry(self.root, show="*")
        self.password.pack()

        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)

        forgot_password = tk.Label(
            self.root,
            text="Forgot password?",
            fg="#1d4ed8",
            cursor="hand2",
            font=("Arial", 10, "underline"),
        )
        forgot_password.pack()
        forgot_password.bind("<Button-1>", lambda _event: self.open_forgot_password_dialog())

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
        email = user["email"]
        messagebox.showinfo("Success", f"Welcome {display_name} ({role.title()})")

        # Admin and staff share the same catalog management permissions. This is
        # the role gate that controls who can add, edit, and delete books.
        if self._can_manage_books(role):
            self.open_inventory_window()
        else:
            self.open_customer_dashboard(display_name, email)

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

        LoginApp(
            self.root,
            self.inventory_service,
            self.orders_service,
            self.auth_service,
        )

    def open_customer_dashboard(self, username, email):
        """
        Open the customer dashboard using the same shared inventory data that
        staff manages, so new books appear immediately for customers too.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

        customer = self.orders_service.ensure_customer(username, email)
        customer_window = CustomerWindow(
            self.root,
            username,
            self.inventory_service,
            self.orders_service,
            customer.customer_id,
            self.show_login_screen,
        )
        customer_window.pack(fill="both", expand=True)

    def open_forgot_password_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Reset Customer Password")
        dialog.geometry("380x280")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(
            dialog,
            text="Customer Password Reset",
            font=("Arial", 14, "bold"),
        ).pack(pady=(16, 8))
        tk.Label(
            dialog,
            text="Enter your customer username, email, and a new password.",
            wraplength=320,
            justify="center",
        ).pack(pady=(0, 12))

        form = tk.Frame(dialog)
        form.pack(fill="x", padx=24)

        username_var = tk.StringVar(value=self.username.get().strip())
        email_var = tk.StringVar(value="")
        new_password_var = tk.StringVar(value="")
        confirm_password_var = tk.StringVar(value="")
        status_var = tk.StringVar(value="")

        fields = [
            ("Username", username_var, False),
            ("Email", email_var, False),
            ("New Password", new_password_var, True),
            ("Confirm Password", confirm_password_var, True),
        ]

        for label_text, variable, hide_text in fields:
            tk.Label(form, text=label_text, anchor="w").pack(fill="x")
            tk.Entry(form, textvariable=variable, show="*" if hide_text else "").pack(
                fill="x",
                pady=(0, 10),
            )

        tk.Label(dialog, textvariable=status_var, fg="#b42318", wraplength=320).pack(
            padx=24,
            pady=(0, 10),
        )

        def submit_reset():
            is_reset, message = self.auth_service.reset_customer_password(
                username_var.get(),
                email_var.get(),
                new_password_var.get(),
                confirm_password_var.get(),
            )
            if not is_reset:
                status_var.set(message)
                return

            messagebox.showinfo("Password Reset", message, parent=dialog)
            dialog.destroy()

        tk.Button(dialog, text="Reset Password", command=submit_reset).pack(
            pady=(0, 16)
        )
