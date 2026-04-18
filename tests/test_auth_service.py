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
    
    def test_username_is_case_insensitive(self):
        is_valid, message, user = self.service.authenticate("MANAGER", "securepass")
        self.assertTrue(is_valid)

if __name__ == "__main__":
    unittest.main()
