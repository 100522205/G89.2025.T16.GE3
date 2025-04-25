"""test_singleton_deposit_store_tests"""
import unittest

from uc3m_money.storage.deposit_json_store import DepositJsonStore
from uc3m_money.storage.json_store import JsonStore


class MyTestCase(unittest.TestCase):
    """test class for balance store singleton"""
    def test_singleton_deposit_store(self):
        """tests method"""


        deposit_store_1 = DepositJsonStore()
        deposit_store_2 = DepositJsonStore()
        deposit_store_3 = DepositJsonStore()

        self.assertEqual(deposit_store_1, deposit_store_2)
        self.assertEqual(deposit_store_2, deposit_store_3)
        self.assertEqual(deposit_store_3, deposit_store_1)

        json_store_1 = JsonStore()
        json_store_2 = JsonStore()

        self.assertNotEqual(json_store_1, json_store_2)


if __name__ == '__main__':
    unittest.main()
