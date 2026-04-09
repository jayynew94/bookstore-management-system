import tkinter as tk
from tkinter import ttk


class OrdersWindow(ttk.Frame):
    def __init__(self, master, inventory_service, orders_service, on_back):
        super().__init__(master, padding=24)
        self.inventory_service = inventory_service
        self.orders_service = orders_service
        self.on_back = on_back
        self.selected_order_id = None
        self.sales_status_var = tk.StringVar(value="Showing all recorded sales.")
        self.start_date_var = tk.StringVar(value="")
        self.end_date_var = tk.StringVar(value="")
        self.detail_vars = {
            "order_id": tk.StringVar(value="No sale selected"),
            "customer": tk.StringVar(value="-"),
            "book": tk.StringVar(value="-"),
            "quantity": tk.StringVar(value="-"),
            "total": tk.StringVar(value="-"),
            "status": tk.StringVar(value="-"),
            "created_at": tk.StringVar(value="-"),
        }

        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(2, weight=1)

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

        order_entry_frame = ttk.LabelFrame(self, text="Create Sale", padding=12)
        order_entry_frame.grid(row=1, column=1, sticky="ew")
        order_entry_frame.columnconfigure(0, weight=1)

        order_form = ttk.Frame(order_entry_frame)
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
        ttk.Label(order_entry_frame, textvariable=self.status_var, foreground="#b42318").grid(
            row=1, column=0, sticky="w", pady=(12, 0)
        )

        sales_frame = ttk.LabelFrame(self, text="Sales History", padding=12)
        sales_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(18, 0))
        sales_frame.columnconfigure(0, weight=3)
        sales_frame.columnconfigure(1, weight=2)
        sales_frame.rowconfigure(1, weight=1)

        filter_frame = ttk.Frame(sales_frame)
        filter_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        filter_frame.columnconfigure(1, weight=1)
        filter_frame.columnconfigure(3, weight=1)

        ttk.Label(filter_frame, text="Start Date").grid(row=0, column=0, sticky="w", padx=(0, 8))
        ttk.Entry(filter_frame, textvariable=self.start_date_var).grid(row=0, column=1, sticky="ew")
        ttk.Label(filter_frame, text="End Date").grid(row=0, column=2, sticky="w", padx=(12, 8))
        ttk.Entry(filter_frame, textvariable=self.end_date_var).grid(row=0, column=3, sticky="ew")
        ttk.Button(filter_frame, text="Apply Filter", command=self.apply_sales_filter).grid(
            row=0, column=4, padx=(12, 0)
        )
        ttk.Button(filter_frame, text="Clear", command=self.clear_sales_filter).grid(
            row=0, column=5, padx=(8, 0)
        )
        ttk.Label(filter_frame, textvariable=self.sales_status_var).grid(
            row=1, column=0, columnspan=6, sticky="w", pady=(10, 0)
        )

        sales_table_frame = ttk.Frame(sales_frame)
        sales_table_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 12))
        sales_table_frame.columnconfigure(0, weight=1)
        sales_table_frame.rowconfigure(0, weight=1)

        self.orders_tree = ttk.Treeview(
            sales_table_frame,
            columns=("customer", "book", "quantity", "total", "status", "date"),
            show="headings",
            height=9,
        )
        for column, heading, width in [
            ("customer", "Customer", 140),
            ("book", "Book", 160),
            ("quantity", "Qty", 60),
            ("total", "Total", 90),
            ("status", "Status", 100),
            ("date", "Date", 100),
        ]:
            self.orders_tree.heading(column, text=heading)
            self.orders_tree.column(column, width=width, anchor="w")
        self.orders_tree.grid(row=0, column=0, sticky="nsew")
        self.orders_tree.bind("<<TreeviewSelect>>", self.handle_order_selection)

        detail_frame = ttk.LabelFrame(sales_frame, text="Sale Detail View", padding=12)
        detail_frame.grid(row=1, column=1, sticky="nsew")
        detail_frame.columnconfigure(1, weight=1)

        for row_index, (label, key) in enumerate(
            [
                ("Order ID", "order_id"),
                ("Customer", "customer"),
                ("Book", "book"),
                ("Quantity", "quantity"),
                ("Total", "total"),
                ("Status", "status"),
                ("Date", "created_at"),
            ]
        ):
            ttk.Label(detail_frame, text=f"{label}:").grid(
                row=row_index, column=0, sticky="nw", padx=(0, 10), pady=5
            )
            ttk.Label(detail_frame, textvariable=self.detail_vars[key], wraplength=240).grid(
                row=row_index, column=1, sticky="nw", pady=5
            )

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
            self.orders_service.place_order(customer_id, book_id, quantity, status="Completed")
        except ValueError as error:
            self.status_var.set(str(error))
            return

        self.quantity_entry.delete(0, "end")
        self.status_var.set("Order placed successfully.")
        self.clear_sales_filter()
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

    def _refresh_orders(self, orders=None):
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)

        orders = self.orders_service.list_orders() if orders is None else orders
        for order in orders:
            self.orders_tree.insert(
                "",
                "end",
                iid=order.order_id,
                values=(
                    order.customer_name,
                    order.book_title,
                    order.quantity,
                    f"${order.total:.2f}",
                    order.status,
                    order.created_at,
                ),
            )

    def handle_order_selection(self, _event=None):
        selected = self.orders_tree.selection()
        if not selected:
            self.selected_order_id = None
            self._clear_order_detail()
            return

        self.selected_order_id = selected[0]
        order = self.orders_service.get_order(self.selected_order_id)
        self.detail_vars["order_id"].set(order.order_id)
        self.detail_vars["customer"].set(order.customer_name)
        self.detail_vars["book"].set(order.book_title)
        self.detail_vars["quantity"].set(str(order.quantity))
        self.detail_vars["total"].set(f"${order.total:.2f}")
        self.detail_vars["status"].set(order.status)
        self.detail_vars["created_at"].set(order.created_at)

    def apply_sales_filter(self):
        orders = self.orders_service.filter_orders(
            self.start_date_var.get(),
            self.end_date_var.get(),
        )
        self._refresh_orders(orders)
        self._clear_order_detail()
        self.selected_order_id = None
        if orders:
            self.sales_status_var.set(f"Showing {len(orders)} filtered sale(s).")
        else:
            self.sales_status_var.set("No sales found.")

    def clear_sales_filter(self):
        self.start_date_var.set("")
        self.end_date_var.set("")
        self.sales_status_var.set("Showing all recorded sales.")
        self._refresh_orders()
        self._clear_order_detail()

    def _clear_order_detail(self):
        self.detail_vars["order_id"].set("No sale selected")
        self.detail_vars["customer"].set("-")
        self.detail_vars["book"].set("-")
        self.detail_vars["quantity"].set("-")
        self.detail_vars["total"].set("-")
        self.detail_vars["status"].set("-")
        self.detail_vars["created_at"].set("-")
