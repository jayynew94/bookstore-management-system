from tkinter import ttk


class CustomerWindow(ttk.Frame):
    def __init__(self, master, username, inventory_service, on_logout):
        super().__init__(master, padding=24)
        self.columnconfigure(0, weight=1)

        header = ttk.Frame(self)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        header.columnconfigure(0, weight=1)

        ttk.Label(
            header,
            text=f"Welcome, {username}",
            font=("Arial", 16, "bold"),
        ).grid(row=0, column=0, sticky="w")
        ttk.Button(header, text="Logout", command=on_logout).grid(row=0, column=1, sticky="e")

        ttk.Label(
            self,
            text="Customer view: browse the current catalog below. Staff-only tools are restricted.",
        ).grid(row=1, column=0, sticky="w", pady=(0, 12))

        catalog = ttk.Treeview(
            self,
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
            catalog.heading(column, text=heading)
            catalog.column(column, width=width, anchor="w")
        catalog.grid(row=2, column=0, sticky="nsew")

        for book in inventory_service.list_books():
            catalog.insert(
                "",
                "end",
                values=(book.title, book.author, book.genre, f"${book.price:.2f}", book.quantity),
            )
