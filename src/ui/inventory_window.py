import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class InventoryWindow(ttk.Frame):
    def __init__(self, master, inventory_service, on_back):
        super().__init__(master, padding=24)
        self.inventory_service = inventory_service
        self.on_back = on_back
        self.selected_book_id = None

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        header_frame.columnconfigure(0, weight=1)

        ttk.Label(
            header_frame,
            text="Inventory",
            font=("Arial", 16, "bold"),
        ).grid(row=0, column=0, sticky="w")

        ttk.Button(
            header_frame,
            text="Back to Dashboard",
            command=self.on_back
        ).grid(row=0, column=1, sticky="e")

        content_frame = ttk.Frame(self)
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        content_frame.rowconfigure(1, weight=0)

        inventory_frame = ttk.LabelFrame(content_frame, text="Current Titles", padding=12)
        inventory_frame.grid(row=0, column=0, sticky="nsew")
        inventory_frame.columnconfigure(0, weight=1)
        inventory_frame.rowconfigure(0, weight=1)

        columns = ("title", "author", "genre", "price", "quantity")
        self.tree = ttk.Treeview(inventory_frame, columns=columns, show="headings", height=10)

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

        search_frame = ttk.LabelFrame(content_frame, text="Search Inventory", padding=12)
        search_frame.grid(row=1, column=0, sticky="ew", pady=(12, 0))
        search_frame.columnconfigure(1, weight=1)

        ttk.Label(search_frame, text="Title Keyword:").grid(
            row=0, column=0, sticky="w", padx=(0, 8)
        )

        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=(0, 8))

        ttk.Button(
            search_frame,
            text="Search",
            command=self.search_by_title
        ).grid(row=0, column=2, padx=(0, 8))

        ttk.Button(
            search_frame,
            text="Show All",
            command=self.show_all_books
        ).grid(row=0, column=3)

        self.status_var = tk.StringVar(value="")
        ttk.Label(self, textvariable=self.status_var, foreground="#b42318").grid(
            row=2, column=0, sticky="w", pady=(12, 0)
        )

        self.refresh_books()

    def refresh_books(self, books=None):
        """
        Refresh the inventory tree.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)

        if books is None:
            books = self.inventory_service.list_books()

        for book in books:
            self.tree.insert(
                "",
                "end",
                iid=book.book_id,
                values=(
                    book.title,
                    book.author,
                    getattr(book, "genre", "General"),
                    f"${book.price:.2f}",
                    book.quantity,
                ),
            )

    def handle_selection(self, _event=None):
        """
        Handle selection of a book in the inventory tree.
        """
        selected_items = self.tree.selection()

        if not selected_items:
            self.selected_book_id = None
            return

        self.selected_book_id = selected_items[0]

    def search_by_title(self):
        """
        Search inventory by title keyword.
        """
        keyword = self.search_entry.get().strip().lower()

        if not keyword:
            self.status_var.set("Enter a title keyword to search.")
            return

        matching_books = []

        for book in self.inventory_service.list_books():
            if keyword in book.title.lower():
                matching_books.append(book)

        self.refresh_books(matching_books)

        if matching_books:
            self.status_var.set(f"Found {len(matching_books)} matching book(s).")
        else:
            self.status_var.set("No books found with that title keyword.")

        self.selected_book_id = None

    def show_all_books(self):
        """
        Reset search and show all books.
        """
        self.search_entry.delete(0, "end")
        self.refresh_books()
        self.status_var.set("Showing all books.")
        self.selected_book_id = None