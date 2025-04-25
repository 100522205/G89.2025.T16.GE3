"""test_singleton_transfer_store_tests"""
import unittest

from uc3m_money.storage.transfer_request_json_store import TransferRequestJsonStore
from uc3m_money.storage.json_store import JsonStore

class MyTestCase(unittest.TestCase):
    """test class for balance store singleton"""
    def test_singleton_transfer_store(self):
        """tests method"""


        transfer_store_1 = TransferRequestJsonStore()
        transfer_store_2 = TransferRequestJsonStore()
        transfer_store_3 = TransferRequestJsonStore()

        self.assertEqual(transfer_store_1, transfer_store_2)
        self.assertEqual(transfer_store_2, transfer_store_3)
        self.assertEqual(transfer_store_3, transfer_store_1)

        json_store_1 = JsonStore()
        json_store_2 = JsonStore()

        self.assertNotEqual(json_store_1, json_store_2)


if __name__ == '__main__':
    unittest.main()
