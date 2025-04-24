from uc3m_money.storage.json_store import JsonStore
from uc3m_money.account_management_config import DEPOSITS_STORE_FILE

class DepositJsonStore(JsonStore):
    def __init__(self):
        super().__init__()
        self._file_name = DEPOSITS_STORE_FILE
        self.load_list_from_file(fnf_error=False)