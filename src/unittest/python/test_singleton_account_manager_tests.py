"""test_singleton_account_manager_tests"""
import unittest

from uc3m_money.account_manager import AccountManager
from uc3m_money.storage.json_store import JsonStore

class MyTestCase(unittest.TestCase):
    """test class for singleton account manager"""
    def test_singleton_account_manager(self):
        """test method"""

        account_manager_1 = AccountManager()
        account_manager_2 = AccountManager()
        account_manager_3 = AccountManager()

        self.assertEqual(account_manager_1, account_manager_2)
        self.assertEqual(account_manager_2, account_manager_3)
        self.assertEqual(account_manager_3, account_manager_1)

        json_store_1 = JsonStore()
        json_store_2 = JsonStore()

        self.assertNotEqual(json_store_1, json_store_2)


if __name__ == '__main__':
    unittest.main()
