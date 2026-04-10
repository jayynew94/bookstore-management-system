import tkinter as tk
from tkinter import ttk


class CustomerWindow(ttk.Frame):
    def __init__(self, master, username, inventory_service, orders_service, customer_id, on_logout):
        super().__init__(master, padding=24)
        self.inventory_service = inventory_service
        self.orders_service = orders_service
        self.customer_id = customer_id
        self.status_var = tk.StringVar(value="")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)

        header = ttk.Frame(self)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 18))
        header.columnconfigure(0, weight=1)

        ttk.Label(
            header,
            text=f"Welcome, {username}",
            font=("Arial", 16, "bold"),
        ).grid(row=0, column=0, sticky="w")
        ttk.Button(header, text="Logout", command=on_logout).grid(row=0, column=1, sticky="e")

        ttk.Label(
            self,
            text="Browse the catalog, place an order, and track your order statuses below.",
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 12))

        catalog_frame = ttk.LabelFrame(self, text="Catalog", padding=12)
        catalog_frame.grid(row=2, column=0, sticky="nsew", padx=(0, 12))
        catalog_frame.columnconfigure(0, weight=1)

        self.catalog = ttk.Treeview(
            catalog_frame,
            columns=("title", "author", "genre", "price", "quantity"),
            show="headings",
            height=10,
        )
        for column, heading, width in [
            ("title", "Title", 170),
            ("author", "Author", 150),
            ("genre", "Genre", 120),
            ("price", "Price", 80),
            ("quantity", "Qty", 60),
        ]:
            self.catalog.heading(column, text=heading)
            self.catalog.column(column, width=width, anchor="w")
        self.catalog.grid(row=0, column=0, sticky="nsew")

        actions_frame = ttk.LabelFrame(self, text="Place Customer Order", padding=12)
        actions_frame.grid(row=2, column=1, sticky="nsew")
        actions_frame.columnconfigure(1, weight=1)

        ttk.Label(actions_frame, text="Book").grid(row=0, column=0, sticky="w", padx=(0, 8))
        self.book_var = tk.StringVar()
        self.book_combo = ttk.Combobox(actions_frame, textvariable=self.book_var, state="readonly")
        self.book_combo.grid(row=0, column=1, sticky="ew", pady=4)

        ttk.Label(actions_frame, text="Quantity").grid(row=1, column=0, sticky="w", padx=(0, 8))
        self.quantity_entry = ttk.Entry(actions_frame)
        self.quantity_entry.grid(row=1, column=1, sticky="ew", pady=4)

        ttk.Button(actions_frame, text="Place Order", command=self.place_order).grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0)
        )

        ttk.Label(actions_frame, textvariable=self.status_var, foreground="#b42318").grid(
            row=3, column=0, columnspan=2, sticky="w", pady=(10, 0)
        )

        history_frame = ttk.LabelFrame(self, text="My Orders", padding=12)
        history_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(18, 0))
        history_frame.columnconfigure(0, weight=1)

        self.orders_tree = ttk.Treeview(
            history_frame,
            columns=("book", "quantity", "total", "status", "date"),
            show="headings",
            height=7,
        )
        for column, heading, width in [
            ("book", "Book", 180),
            ("quantity", "Qty", 60),
            ("total", "Total", 90),
            ("status", "Status", 110),
            ("date", "Date", 100),
        ]:
            self.orders_tree.heading(column, text=heading)
            self.orders_tree.column(column, width=width, anchor="w")
        self.orders_tree.grid(row=0, column=0, sticky="nsew")

        self.refresh_data()

    def refresh_data(self):
        for item in self.catalog.get_children():
            self.catalog.delete(item)

        books = self.inventory_service.list_books()
        book_options = []
        for book in books:
            self.catalog.insert(
                "",
                "end",
                values=(book.title, book.author, book.genre, f"${book.price:.2f}", book.quantity),
            )
            book_options.append(f"{book.title} ({book.quantity} in stock)")

        self.book_combo["values"] = book_options
        if book_options:
            self.book_combo.current(0)
        else:
            self.book_var.set("")

        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)

        for order in self.orders_service.filter_orders(customer_id=self.customer_id):
            self.orders_tree.insert(
                "",
                "end",
                values=(order.book_title, order.quantity, f"${order.total:.2f}", order.status, order.created_at),
            )

    def place_order(self):
        selected_index = self.book_combo.current()
        if selected_index < 0:
            self.status_var.set("Select a book before placing an order.")
            return

        books = self.inventory_service.list_books()
        try:
            quantity = int(self.quantity_entry.get())
            self.orders_service.place_order(
                self.customer_id,
                books[selected_index].book_id,
                quantity,
                status="Submitted",
            )
        except ValueError as error:
            self.status_var.set(str(error))
            return

        self.quantity_entry.delete(0, "end")
        self.status_var.set("Customer order placed successfully.")
        self.refresh_data()
