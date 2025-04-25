"""input_deposit_json_store module"""
from uc3m_money.storage.json_store import JsonStore

class InputDepositJsonStore(JsonStore):
    """input deposit json store subclass"""
    def __init__(self, input_file):
        super().__init__()
        self._file_name = input_file
