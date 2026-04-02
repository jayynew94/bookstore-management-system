import tkinter as tk
from tkinter import ttk


class OrdersWindow(ttk.Frame):
    def __init__(self, master, inventory_service, orders_service, on_back):
        super().__init__(master, padding=24)
        self.inventory_service = inventory_service
        self.orders_service = orders_service
        self.on_back = on_back

        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(1, weight=1)

        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 18))
        header_frame.columnconfigure(0, weight=1)

        ttk.Label(header_frame, text="Orders and Customers", font=("Arial", 16, "bold")).grid(
            row=0, column=0, sticky="w"
        )
        ttk.Button(header_frame, text="Back to Dashboard", command=self.on_back).grid(
            row=0, column=1, sticky="e"
        )

        customer_frame = ttk.LabelFrame(self, text="Customers", padding=12)
        customer_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 12))
        customer_frame.columnconfigure(0, weight=1)

        self.customers_tree = ttk.Treeview(
            customer_frame,
            columns=("name", "email"),
            show="headings",
            height=8,
        )
        self.customers_tree.heading("name", text="Name")
        self.customers_tree.heading("email", text="Email")
        self.customers_tree.column("name", width=170, anchor="w")
        self.customers_tree.column("email", width=210, anchor="w")
        self.customers_tree.grid(row=0, column=0, sticky="nsew")

        customer_form = ttk.Frame(customer_frame)
        customer_form.grid(row=1, column=0, sticky="ew", pady=(12, 0))
        customer_form.columnconfigure(1, weight=1)

        ttk.Label(customer_form, text="Name").grid(row=0, column=0, sticky="w", padx=(0, 8))
        self.customer_name_entry = ttk.Entry(customer_form)
        self.customer_name_entry.grid(row=0, column=1, sticky="ew", pady=4)
        ttk.Label(customer_form, text="Email").grid(row=1, column=0, sticky="w", padx=(0, 8))
        self.customer_email_entry = ttk.Entry(customer_form)
        self.customer_email_entry.grid(row=1, column=1, sticky="ew", pady=4)
        ttk.Button(customer_form, text="Add Customer", command=self.add_customer).grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=(8, 0)
        )

        orders_frame = ttk.LabelFrame(self, text="Place and Review Orders", padding=12)
        orders_frame.grid(row=1, column=1, sticky="nsew")
        orders_frame.columnconfigure(0, weight=1)

        order_form = ttk.Frame(orders_frame)
        order_form.grid(row=0, column=0, sticky="ew")
        order_form.columnconfigure(1, weight=1)

        ttk.Label(order_form, text="Customer").grid(row=0, column=0, sticky="w", padx=(0, 8))
        self.customer_var = tk.StringVar()
        self.customer_combo = ttk.Combobox(order_form, textvariable=self.customer_var, state="readonly")
        self.customer_combo.grid(row=0, column=1, sticky="ew", pady=4)

        ttk.Label(order_form, text="Book").grid(row=1, column=0, sticky="w", padx=(0, 8))
        self.book_var = tk.StringVar()
        self.book_combo = ttk.Combobox(order_form, textvariable=self.book_var, state="readonly")
        self.book_combo.grid(row=1, column=1, sticky="ew", pady=4)

        ttk.Label(order_form, text="Quantity").grid(row=2, column=0, sticky="w", padx=(0, 8))
        self.quantity_entry = ttk.Entry(order_form)
        self.quantity_entry.grid(row=2, column=1, sticky="ew", pady=4)

        ttk.Button(order_form, text="Place Order", command=self.place_order).grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=(8, 0)
        )

        self.status_var = tk.StringVar(value="")
        ttk.Label(orders_frame, textvariable=self.status_var, foreground="#b42318").grid(
            row=1, column=0, sticky="w", pady=(12, 8)
        )

        self.orders_tree = ttk.Treeview(
            orders_frame,
            columns=("customer", "book", "quantity", "total"),
            show="headings",
            height=9,
        )
        for column, heading, width in [
            ("customer", "Customer", 140),
            ("book", "Book", 160),
            ("quantity", "Qty", 60),
            ("total", "Total", 90),
        ]:
            self.orders_tree.heading(column, text=heading)
            self.orders_tree.column(column, width=width, anchor="w")
        self.orders_tree.grid(row=2, column=0, sticky="nsew")

        self._customer_options = {}
        self._book_options = {}
        self.refresh_data()

    def refresh_data(self):
        self._refresh_customers()
        self._refresh_books()
        self._refresh_orders()

    def add_customer(self):
        try:
            self.orders_service.add_customer(
                self.customer_name_entry.get(),
                self.customer_email_entry.get(),
            )
        except ValueError as error:
            self.status_var.set(str(error))
            return

        self.customer_name_entry.delete(0, "end")
        self.customer_email_entry.delete(0, "end")
        self.status_var.set("Customer added successfully.")
        self.refresh_data()

    def place_order(self):
        customer_id = self._customer_options.get(self.customer_var.get())
        book_id = self._book_options.get(self.book_var.get())

        if not customer_id or not book_id:
            self.status_var.set("Select both a customer and a book.")
            return

        try:
            quantity = int(self.quantity_entry.get())
            self.orders_service.place_order(customer_id, book_id, quantity)
        except ValueError as error:
            self.status_var.set(str(error))
            return

        self.quantity_entry.delete(0, "end")
        self.status_var.set("Order placed successfully.")
        self.refresh_data()

    def _refresh_customers(self):
        for item in self.customers_tree.get_children():
            self.customers_tree.delete(item)

        customers = self.orders_service.list_customers()
        self._customer_options = {
            f"{customer.name} ({customer.email})": customer.customer_id for customer in customers
        }
        self.customer_combo["values"] = list(self._customer_options.keys())
        if self.customer_combo["values"]:
            if self.customer_var.get() not in self._customer_options:
                self.customer_combo.current(0)
        else:
            self.customer_var.set("")

        for customer in customers:
            self.customers_tree.insert("", "end", values=(customer.name, customer.email))

    def _refresh_books(self):
        books = self.inventory_service.list_books()
        self._book_options = {
            f"{book.title} ({book.quantity} in stock)": book.book_id for book in books
        }
        self.book_combo["values"] = list(self._book_options.keys())
        if self.book_combo["values"]:
            if self.book_var.get() not in self._book_options:
                self.book_combo.current(0)
        else:
            self.book_var.set("")

    def _refresh_orders(self):
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)

        for order in self.orders_service.list_orders():
            self.orders_tree.insert(
                "",
                "end",
                values=(order.customer_name, order.book_title, order.quantity, f"${order.total:.2f}"),
            )
