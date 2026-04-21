import unittest

from services.auth_service import AuthService


class AuthServiceTests(unittest.TestCase):
    def setUp(self):
        self.service = AuthService()

    def test_rejects_missing_username_or_password(self):
        is_valid, message, user = self.service.authenticate("", "")
        self.assertFalse(is_valid)
        self.assertEqual(message, "Please enter both username and password.")
        self.assertIsNone(user)

    def test_rejects_invalid_credentials(self):
        is_valid, message, user = self.service.authenticate("manager", "wrongpass")
        self.assertFalse(is_valid)
        self.assertEqual(message, "Invalid username or password.")
        self.assertIsNone(user)

    def test_accepts_valid_admin_credentials(self):
        is_valid, message, user = self.service.authenticate("admin", "admin123")
        self.assertTrue(is_valid)
        self.assertEqual(message, "")
        self.assertEqual(user["role"], "admin")
        self.assertEqual(user["display_name"], "System Admin")

    def test_accepts_valid_staff_credentials(self):
        is_valid, message, user = self.service.authenticate("staff1", "books123")
        self.assertTrue(is_valid)
        self.assertEqual(message, "")
        self.assertEqual(user["role"], "staff")
        self.assertEqual(user["display_name"], "Inventory Staff")

    def test_accepts_valid_customer_credentials(self):
        is_valid, message, user = self.service.authenticate("customer1", "reader123")
        self.assertTrue(is_valid)
        self.assertEqual(message, "")
        self.assertEqual(user["role"], "customer")

    def test_resets_customer_password_when_email_matches(self):
        is_reset, message = self.service.reset_customer_password(
            "customer1",
            "customer1@bookstore.local",
            "newpass1",
            "newpass1",
        )

        self.assertTrue(is_reset)
        self.assertEqual(message, "Password reset successfully. You can log in now.")
        is_valid, _, user = self.service.authenticate("customer1", "newpass1")
        self.assertTrue(is_valid)
        self.assertEqual(user["role"], "customer")

    def test_rejects_password_reset_for_non_customer_accounts(self):
        is_reset, message = self.service.reset_customer_password(
            "staff1",
            "staff1@bookstore.local",
            "newpass1",
            "newpass1",
        )

        self.assertFalse(is_reset)
        self.assertEqual(message, "Only customer accounts can reset passwords here.")

    def test_rejects_password_reset_with_wrong_email(self):
        is_reset, message = self.service.reset_customer_password(
            "customer1",
            "wrong@bookstore.local",
            "newpass1",
            "newpass1",
        )

        self.assertFalse(is_reset)
        self.assertEqual(message, "Email does not match the selected customer account.")
    
    def test_username_is_case_insensitive(self):
        is_valid, message, user = self.service.authenticate("MANAGER", "securepass")
        self.assertTrue(is_valid)

if __name__ == "__main__":
    unittest.main()
