import tkinter as tk
from tkinter import ttk


class InventoryWindow(ttk.Frame):
    def __init__(self, master, inventory_service, on_back):
        super().__init__(master, padding=24)
        self.inventory_service = inventory_service
        self.on_back = on_back
        self.selected_book_id = None
        self.detail_vars = {
            "title": tk.StringVar(value="No book selected"),
            "author": tk.StringVar(value="-"),
            "genre": tk.StringVar(value="-"),
            "price": tk.StringVar(value="-"),
            "quantity": tk.StringVar(value="-"),
            "isbn": tk.StringVar(value="-"),
        }
        self.search_var = tk.StringVar(value="")
        self.search_field_var = tk.StringVar(value="isbn")
        self.results_var = tk.StringVar(value="Showing all books.")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        header_frame.columnconfigure(0, weight=1)

        ttk.Label(
            header_frame,
            text="Inventory",
            font=("Arial", 16, "bold"),
        ).grid(row=0, column=0, sticky="w")
        ttk.Button(header_frame, text="Back to Dashboard", command=self.on_back).grid(
            row=0, column=1, sticky="e"
        )

        search_frame = ttk.LabelFrame(self, text="Search Inventory", padding=12)
        search_frame.grid(row=1, column=0, sticky="ew", pady=(0, 18))
        search_frame.columnconfigure(3, weight=1)

        ttk.Label(search_frame, text="Search By").grid(row=0, column=0, sticky="w", padx=(0, 8))
        ttk.Combobox(
            search_frame,
            textvariable=self.search_field_var,
            values=("title", "author", "isbn"),
            state="readonly",
            width=12,
        ).grid(row=0, column=1, sticky="w")
        ttk.Label(search_frame, text="Keyword").grid(row=0, column=2, sticky="w", padx=(18, 8))
        ttk.Entry(search_frame, textvariable=self.search_var).grid(row=0, column=3, sticky="ew")
        ttk.Button(search_frame, text="Search", command=self.apply_search).grid(
            row=0, column=4, padx=(12, 0)
        )
        ttk.Button(search_frame, text="Clear", command=self.clear_search).grid(
            row=0, column=5, padx=(8, 0)
        )
        ttk.Label(search_frame, textvariable=self.results_var).grid(
            row=1, column=0, columnspan=6, sticky="w", pady=(10, 0)
        )

        content_frame = ttk.Frame(self)
        content_frame.grid(row=2, column=0, sticky="nsew")
        content_frame.columnconfigure(0, weight=3)
        content_frame.columnconfigure(1, weight=2)
        content_frame.rowconfigure(0, weight=1)

        inventory_frame = ttk.LabelFrame(content_frame, text="Current Titles", padding=12)
        inventory_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        inventory_frame.columnconfigure(0, weight=1)
        inventory_frame.rowconfigure(0, weight=1)

        columns = ("title", "author", "genre", "price", "quantity")
        self.tree = ttk.Treeview(inventory_frame, columns=columns, show="headings", height=8)
        for column, heading, width in [
            ("title", "Title", 170),
            ("author", "Author", 150),
            ("genre", "Genre", 120),
            ("price", "Price", 80),
            ("quantity", "Qty", 60),
        ]:
            self.tree.heading(column, text=heading)
            self.tree.column(column, width=width, anchor="w")
        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(inventory_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.bind("<<TreeviewSelect>>", self.handle_selection)

        detail_frame = ttk.LabelFrame(content_frame, text="Book Detail View", padding=12)
        detail_frame.grid(row=0, column=1, sticky="nsew")
        detail_frame.columnconfigure(1, weight=1)

        for row_index, (label, key) in enumerate(
            [
                ("Title", "title"),
                ("Author", "author"),
                ("Genre", "genre"),
                ("Price", "price"),
                ("Quantity", "quantity"),
                ("ISBN", "isbn"),
            ]
        ):
            ttk.Label(detail_frame, text=f"{label}:").grid(
                row=row_index,
                column=0,
                sticky="nw",
                padx=(0, 10),
                pady=6,
            )
            ttk.Label(
                detail_frame,
                textvariable=self.detail_vars[key],
                wraplength=220,
                justify="left",
            ).grid(row=row_index, column=1, sticky="nw", pady=6)

        form_frame = ttk.LabelFrame(self, text="Book Details", padding=12)
        form_frame.grid(row=3, column=0, sticky="ew", pady=(18, 0))
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)

        self.inputs = {}
        fields = [
            ("Title", "title"),
            ("Author", "author"),
            ("Genre", "genre"),
            ("Price", "price"),
            ("Quantity", "quantity"),
            ("ISBN", "isbn"),
        ]

        for index, (label, key) in enumerate(fields):
            row = index // 2
            column = (index % 2) * 2
            ttk.Label(form_frame, text=label).grid(
                row=row, column=column, sticky="w", padx=(0, 8), pady=6
            )
            entry = ttk.Entry(form_frame)
            entry.grid(row=row, column=column + 1, sticky="ew", pady=6, padx=(0, 16))
            self.inputs[key] = entry

        self.status_var = tk.StringVar(value="")
        ttk.Label(form_frame, textvariable=self.status_var, foreground="#b42318").grid(
            row=3, column=0, columnspan=4, sticky="w", pady=(8, 4)
        )
        actions_frame = ttk.Frame(form_frame)
        actions_frame.grid(row=4, column=0, columnspan=4, sticky="ew", pady=(8, 0))
        actions_frame.columnconfigure((0, 1, 2), weight=1)
        ttk.Button(actions_frame, text="Add Book", command=self.add_book).grid(
            row=0, column=0, sticky="ew"
        )
        ttk.Button(actions_frame, text="Update Selected", command=self.update_book).grid(
            row=0, column=1, sticky="ew", padx=10
        )
        ttk.Button(actions_frame, text="Delete Selected", command=self.delete_book).grid(
            row=0, column=2, sticky="ew"
        )

        self.refresh_books()

    def refresh_books(self, books=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        books = self.inventory_service.list_books() if books is None else books
        for book in books:
            self.tree.insert(
                "",
                "end",
                iid=book.book_id,
                values=(book.title, book.author, book.genre, f"${book.price:.2f}", book.quantity),
            )

    def handle_selection(self, _event=None):
        selected_items = self.tree.selection()
        if not selected_items:
            self.selected_book_id = None
            self._clear_detail_panel()
            return

        self.selected_book_id = selected_items[0]
        book = self.inventory_service.get_book(self.selected_book_id)
        self._update_detail_panel(book)
        self.inputs["title"].delete(0, "end")
        self.inputs["title"].insert(0, book.title)
        self.inputs["author"].delete(0, "end")
        self.inputs["author"].insert(0, book.author)
        self.inputs["genre"].delete(0, "end")
        self.inputs["genre"].insert(0, book.genre)
        self.inputs["price"].delete(0, "end")
        self.inputs["price"].insert(0, f"{book.price:.2f}")
        self.inputs["quantity"].delete(0, "end")
        self.inputs["quantity"].insert(0, str(book.quantity))
        self.inputs["isbn"].delete(0, "end")
        self.inputs["isbn"].insert(0, book.isbn)
        self.status_var.set(f"Selected '{book.title}'.")

    def add_book(self):
        try:
            self.inventory_service.add_book(*self._form_values())
        except ValueError as error:
            self.status_var.set(str(error))
            return

        self._clear_form()
        self.status_var.set("Book added successfully.")
        self.clear_search()

    def update_book(self):
        if not self.selected_book_id:
            self.status_var.set("Select a book to update.")
            return

        try:
            self.inventory_service.update_book(self.selected_book_id, *self._form_values())
        except ValueError as error:
            self.status_var.set(str(error))
            return

        self.status_var.set("Book updated successfully.")
        self.clear_search()
        self.tree.selection_set(self.selected_book_id)
        self.handle_selection()

    def delete_book(self):
        if not self.selected_book_id:
            self.status_var.set("Select a book to delete.")
            return

        try:
            self.inventory_service.delete_book(self.selected_book_id)
        except ValueError as error:
            self.status_var.set(str(error))
            return

        self._clear_form()
        self.selected_book_id = None
        self._clear_detail_panel()
        self.status_var.set("Book deleted successfully.")
        self.clear_search()

    def _form_values(self):
        return (
            self.inputs["title"].get(),
            self.inputs["author"].get(),
            self.inputs["genre"].get(),
            float(self.inputs["price"].get()),
            int(self.inputs["quantity"].get()),
            self.inputs["isbn"].get(),
        )

    def _clear_form(self):
        for entry in self.inputs.values():
            entry.delete(0, "end")

    def _update_detail_panel(self, book):
        self.detail_vars["title"].set(book.title)
        self.detail_vars["author"].set(book.author)
        self.detail_vars["genre"].set(book.genre)
        self.detail_vars["price"].set(f"${book.price:.2f}")
        self.detail_vars["quantity"].set(str(book.quantity))
        self.detail_vars["isbn"].set(book.isbn or "-")

    def _clear_detail_panel(self):
        self.detail_vars["title"].set("No book selected")
        self.detail_vars["author"].set("-")
        self.detail_vars["genre"].set("-")
        self.detail_vars["price"].set("-")
        self.detail_vars["quantity"].set("-")
        self.detail_vars["isbn"].set("-")

    def apply_search(self):
        books = self.inventory_service.search_books(
            self.search_var.get(),
            self.search_field_var.get(),
        )
        self.refresh_books(books)
        self.selected_book_id = None
        self._clear_detail_panel()
        if books:
            self.results_var.set(f"Showing {len(books)} matching result(s).")
        else:
            self.results_var.set("No results found.")

    def clear_search(self):
        self.search_var.set("")
        self.results_var.set("Showing all books.")
        self.refresh_books()
        self.selected_book_id = None
        self._clear_detail_panel()
