import tkinter as tk
from tkinter import ttk


class InventoryWindow(ttk.Frame):
    def __init__(self, master, inventory_service, on_back):
        super().__init__(master, padding=24)
        self.inventory_service = inventory_service
        self.on_back = on_back
        self.selected_book_id = None

        self.columnconfigure(0, weight=1)

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

        inventory_frame = ttk.LabelFrame(self, text="Current Titles", padding=12)
        inventory_frame.grid(row=1, column=0, sticky="nsew")
        inventory_frame.columnconfigure(0, weight=1)

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

        form_frame = ttk.LabelFrame(self, text="Book Details", padding=12)
        form_frame.grid(row=2, column=0, sticky="ew", pady=(18, 0))
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)

        self.inputs = {}
        fields = [
            ("Title", "title"),
            ("Author", "author"),
            ("Genre", "genre"),
            ("Price", "price"),
            ("Quantity", "quantity"),
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

    def refresh_books(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for book in self.inventory_service.list_books():
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
            return

        self.selected_book_id = selected_items[0]
        book = self.inventory_service.get_book(self.selected_book_id)
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
        self.status_var.set(f"Selected '{book.title}'.")

    def add_book(self):
        try:
            self.inventory_service.add_book(*self._form_values())
        except ValueError as error:
            self.status_var.set(str(error))
            return

        self._clear_form()
        self.status_var.set("Book added successfully.")
        self.refresh_books()

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
        self.refresh_books()
        self.tree.selection_set(self.selected_book_id)

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
        self.status_var.set("Book deleted successfully.")
        self.refresh_books()

    def _form_values(self):
        return (
            self.inputs["title"].get(),
            self.inputs["author"].get(),
            self.inputs["genre"].get(),
            float(self.inputs["price"].get()),
            int(self.inputs["quantity"].get()),
        )

    def _clear_form(self):
        for entry in self.inputs.values():
            entry.delete(0, "end")

