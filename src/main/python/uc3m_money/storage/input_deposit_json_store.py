import json

from uc3m_money.storage.json_store import JsonStore

from uc3m_money.account_management_exception import AccountManagementException


class InputDepositJsonStore(JsonStore):
    def __init__(self, input_file):
        super().__init__()
        self._file_name = input_file

    def load_list_from_file(self, fnf_error):
        try:
            with open(self._file_name, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError as fnf:
            if fnf_error is True:
                raise AccountManagementException("Error: file input not found") from fnf
            else:
                self._data_list = []
        except json.JSONDecodeError as exception:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from exception

        return self._data_list
