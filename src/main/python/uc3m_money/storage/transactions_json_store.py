"""transactions_json_store module"""
from uc3m_money.storage.json_store import JsonStore
from uc3m_money.account_management_config import TRANSACTIONS_STORE_FILE

class TransactionsJsonStore(JsonStore):
    """transactions json store subclass"""
    def __init__(self):
        super().__init__()
        self._file_name = TRANSACTIONS_STORE_FILE
