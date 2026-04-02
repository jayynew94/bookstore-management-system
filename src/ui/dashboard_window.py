from tkinter import ttk


class DashboardWindow(ttk.Frame):
    def __init__(
        self,
        master,
        username,
        inventory_service,
        on_open_inventory,
        orders_service,
        on_open_orders,
        on_logout,
    ):
        super().__init__(master, padding=24)
        self.columnconfigure((0, 1, 2, 3), weight=1)

        header = ttk.Frame(self)
        header.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0, 6))
        header.columnconfigure(0, weight=1)

        title_label = ttk.Label(
            header,
            text=f"Welcome back, {username}",
            font=("Arial", 16, "bold"),
        )
        title_label.grid(row=0, column=0, sticky="w")
        ttk.Button(header, text="Logout", command=on_logout).grid(row=0, column=1, sticky="e")

        subtitle_label = ttk.Label(
            self,
            text="Here is a quick look at inventory and recent order activity.",
        )
        subtitle_label.grid(row=1, column=0, columnspan=4, sticky="w", pady=(0, 18))

        stats = [
            ("Titles", inventory_service.total_titles()),
            ("Units in Stock", inventory_service.total_stock()),
            ("Inventory Value", f"${inventory_service.inventory_value():.2f}"),
            ("Orders", orders_service.total_orders()),
        ]

        for index, (label, value) in enumerate(stats):
            card = ttk.LabelFrame(self, text=label, padding=16)
            card.grid(row=2, column=index, sticky="nsew", padx=(0, 12) if index < 3 else 0)
            ttk.Label(card, text=str(value), font=("Arial", 14, "bold")).pack(anchor="w")

        actions = ttk.LabelFrame(self, text="Next Step", padding=16)
        actions.grid(row=3, column=0, columnspan=4, sticky="ew", pady=(18, 0))
        ttk.Label(
            actions,
            text="Open inventory to manage titles, or open orders to manage customers and sales.",
        ).pack(anchor="w")
        button_row = ttk.Frame(actions)
        button_row.pack(anchor="w", pady=(10, 0))
        ttk.Button(button_row, text="Open Inventory", command=on_open_inventory).pack(side="left")
        ttk.Button(button_row, text="Open Orders", command=on_open_orders).pack(
            side="left", padx=(10, 0)
        )

        revenue_card = ttk.LabelFrame(self, text="Revenue", padding=16)
        revenue_card.grid(row=4, column=0, columnspan=4, sticky="ew", pady=(18, 0))
        ttk.Label(
            revenue_card,
            text=f"Total recorded revenue: ${orders_service.total_revenue():.2f}",
            font=("Arial", 12, "bold"),
        ).pack(anchor="w")
