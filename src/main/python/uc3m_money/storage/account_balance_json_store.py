"""Module for defining a subclass of JsonStore for function 3"""
from uc3m_money.storage.json_store import JsonStore
from uc3m_money.account_management_config import BALANCES_STORE_FILE

class AccountBalanceJsonStore(JsonStore):
    """Subclass of JsonStore for management of json files in function 3"""
    #pylint:disable=invalid-name
    class __AccountBalanceJsonStore(JsonStore):
        def __init__(self):
            super().__init__()
            self._file_name = BALANCES_STORE_FILE
            self.load_list_from_file(fnf_error=False)

        def store_balance(self, balance_dict):
            """initialization of the functionalities for storing jsons in function 3"""
            self._data_list.append(balance_dict)
            self.save_list_to_file()

    __instance = None

    def __new__(cls):
        if not AccountBalanceJsonStore.__instance:
            AccountBalanceJsonStore.__instance = AccountBalanceJsonStore.__AccountBalanceJsonStore()
        return AccountBalanceJsonStore.__instance
