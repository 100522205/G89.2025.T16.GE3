"""test_singleton_balance_store_tests"""
import unittest

from uc3m_money.storage.account_balance_json_store import AccountBalanceJsonStore
from uc3m_money.storage.json_store import JsonStore


class MyTestCase(unittest.TestCase):
    """test class for balance store singleton"""
    def test_singleton_balance_store_tests(self):
        """tests method"""


        balance_store_1 = AccountBalanceJsonStore()
        balance_store_2 = AccountBalanceJsonStore()
        balance_store_3 = AccountBalanceJsonStore()

        self.assertEqual(balance_store_1, balance_store_2)
        self.assertEqual(balance_store_2, balance_store_3)
        self.assertEqual(balance_store_3, balance_store_1)

        json_store_1 = JsonStore()
        json_store_2 = JsonStore()

        self.assertNotEqual(json_store_1, json_store_2)


if __name__ == '__main__':
    unittest.main()
