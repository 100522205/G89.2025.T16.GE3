from uc3m_money.storage.json_store import JsonStore
from uc3m_money.account_management_config import BALANCES_STORE_FILE

class AccountBalanceJsonStore(JsonStore):
    def __init__(self):
        super().__init__()
        self._file_name = BALANCES_STORE_FILE
        self.load_list_from_file(fnf_error=False)

    def store_balance(self, balance_dict):
        self._data_list.append(balance_dict)
        self.save_list_to_file()
