import json

from uc3m_money.account_management_config import (TRANSFERS_STORE_FILE,DEPOSITS_STORE_FILE,BALANCES_STORE_FILE,
                                                  TRANSACTIONS_STORE_FILE)
from uc3m_money.account_management_exception import AccountManagementException


class JsonStore:

    _data_list = []
    _file_name = ""

    def __init__(self):
        self._data_list = []
        self._file_name = ""


    def save_list_to_file(self):
        try:
            with open(self._file_name, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as exception:
            raise AccountManagementException("Wrong file  or file path") from exception
        except json.JSONDecodeError as exception:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from exception


    def load_list_from_file(self):
        try:
            with open(self._file_name, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError:
            self._data_list = []
        except json.JSONDecodeError as exception:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from exception


    def add_item(self, item):
        self._data_list.append(item)


    def find_item(self, key, value):
        for instance in self._data_list:
            if self._data_list[key] == value:
                return True


    def save_deposit(deposit_obj):
        try:
            with open(DEPOSITS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                deposit_load = json.load(file)
        except FileNotFoundError as exception:
            deposit_load = []
        except json.JSONDecodeError as exception:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from exception
        deposit_load.append(deposit_obj.to_json())
        try:
            with open(DEPOSITS_STORE_FILE, "w", encoding="utf-8", newline="") as file:
                json.dump(deposit_load, file, indent=2)
        except FileNotFoundError as exception:
            raise AccountManagementException("Wrong file  or file path") from exception
        except json.JSONDecodeError as exception:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from exception


    def save_balance(last_balance):
        try:
            with open(BALANCES_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                balance_list = json.load(file)
        except FileNotFoundError:
            balance_list = []
        except json.JSONDecodeError as exception:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from exception
        balance_list.append(last_balance)
        try:
            with open(BALANCES_STORE_FILE, "w", encoding="utf-8", newline="") as file:
                json.dump(balance_list, file, indent=2)
        except FileNotFoundError as exception:
            raise AccountManagementException("Wrong file  or file path") from exception


    def load_deposit(input_file):
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                input_deposit = json.load(file)
        except FileNotFoundError as exception:
            raise AccountManagementException("Error: file input not found") from exception
        except json.JSONDecodeError as exception:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from exception
        # comprobar valores del fichero
        try:
            deposit_iban = input_deposit["IBAN"]
            deposit_amount = input_deposit["AMOUNT"]
        except KeyError as exception:
            raise AccountManagementException("Error - Invalid Key in JSON") from exception
        return deposit_amount, deposit_iban

    @staticmethod
    def read_transactions_file():
        """loads the content of the transactions file
        and returns a list"""
        try:
            with open(TRANSACTIONS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                input_list = json.load(file)
        except FileNotFoundError as exception:
            raise AccountManagementException("Wrong file  or file path") from exception
        except json.JSONDecodeError as exception:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from exception
        return input_list