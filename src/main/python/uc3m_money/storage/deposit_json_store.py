"""deposit_json_store module"""
from uc3m_money.storage.json_store import JsonStore
from uc3m_money.account_management_config import DEPOSITS_STORE_FILE

class DepositJsonStore(JsonStore):
    """deposit json store subclass"""
    # pylint:disable=invalid-name
    class __DepositJsonStore(JsonStore):
        def __init__(self):
            super().__init__()
            self._file_name = DEPOSITS_STORE_FILE
            self.load_list_from_file(fnf_error=False)

        def store_deposit(self, deposit_obj):
            """store deposit method"""
            self.add_item(deposit_obj)
            self.save_list_to_file()

    __instance = None

    def __new__(cls):
        if not DepositJsonStore.__instance:
            DepositJsonStore.__instance = DepositJsonStore.__DepositJsonStore()
        return DepositJsonStore.__instance
