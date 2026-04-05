from __future__ import annotations


class AuthService:
    def __init__(self):
        self._users = {
            "manager": {
                "password": "securepass",
                "role": "staff",
                "display_name": "Store Manager",
            },
            "staff1": {
                "password": "books123",
                "role": "staff",
                "display_name": "Inventory Staff",
            },
            "customer1": {
                "password": "reader123",
                "role": "customer",
                "display_name": "Customer One",
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
            },
        )

    def demo_users(self) -> list[tuple[str, str]]:
        return [
            ("manager", "securepass"),
            ("staff1", "books123"),
            ("customer1", "reader123"),
        ]