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

    def reset_customer_password(
        self,
        username: str,
        email: str,
        new_password: str,
        confirm_password: str,
    ) -> tuple[bool, str]:
        username = username.strip().lower()
        email = email.strip().lower()
        new_password = new_password.strip()
        confirm_password = confirm_password.strip()

        if not username or not email or not new_password or not confirm_password:
            return False, "All reset fields are required."

        user = self._users.get(username)
        if user is None:
            return False, "Customer account could not be found."

        if user["role"] != "customer":
            return False, "Only customer accounts can reset passwords here."

        if user["email"].lower() != email:
            return False, "Email does not match the selected customer account."

        if new_password != confirm_password:
            return False, "New password and confirmation do not match."

        if len(new_password) < 6:
            return False, "New password must be at least 6 characters long."

        # Update the in-memory auth store so the new password works immediately
        # from the login screen during the same session.
        user["password"] = new_password
        return True, "Password reset successfully. You can log in now."
