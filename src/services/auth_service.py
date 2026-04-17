from __future__ import annotations


class AuthService:
    def __init__(self):
        self._users = {
            "admin": {
                "password": "admin123",
                "role": "admin",
                "display_name": "System Admin",
                "email": "admin@bookstore.local",
            },
            "manager": {
                "password": "securepass",
                "role": "staff",
                "display_name": "Store Manager",
                "email": "manager@bookstore.local",
            },
            "staff1": {
                "password": "books123",
                "role": "staff",
                "display_name": "Inventory Staff",
                "email": "staff1@bookstore.local",
            },
            "customer1": {
                "password": "reader123",
                "role": "customer",
                "display_name": "Customer One",
                "email": "customer1@bookstore.local",
            },
        }

    def authenticate(self, username: str, password: str) -> tuple[bool, str, dict | None]:
        username = username.strip()
        password = password.strip()

        if not username or not password:
            return False, "Please enter both username and password.", None

        user = self._users.get(username.lower())
        if user is None or user["password"] != password:
            return False, "Invalid username or password.", None

        return (
            True,
            "",
            {
                "username": username,
                "display_name": user["display_name"],
                "role": user["role"],
                "email": user["email"],
            },
        )

    def demo_users(self) -> list[tuple[str, str]]:
        return [
            ("admin", "admin123"),
            ("manager", "securepass"),
            ("staff1", "books123"),
            ("customer1", "reader123"),
        ]
