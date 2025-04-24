"JSON superclass to avoid divergent code in account_manager"
import json

from uc3m_money.account_management_config import (DEPOSITS_STORE_FILE,BALANCES_STORE_FILE,
                                                  TRANSACTIONS_STORE_FILE)
from uc3m_money.account_management_exception import AccountManagementException


class JsonStore:
    """superclass for JSON managing code structures"""


    def __init__(self):
        self._data_list = []
        self._file_name = ""


    def save_list_to_file(self):
        """general method of saving data into JSON"""
        try:
            with open(self._file_name, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as exception:
            raise AccountManagementException("Wrong file  or file path") from exception
        except json.JSONDecodeError as exception:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from exception


    def load_list_from_file(self, fnf_error):
        """general method of loading a JSON"""
        try:
            with open(self._file_name, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError as fnf:
            if fnf_error is True:
                raise AccountManagementException("Error: file input not found") from fnf
            self._data_list = []
        except json.JSONDecodeError as exception:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from exception
        return self._data_list

    def add_item(self, item):
        """general method of adding new data to a data tuple"""
        self._data_list.append(item.to_json())


    def find_item(self, key, value):
        """general method for checking duplicates"""
        for instance in self._data_list:
            if instance[key] == value:
                return True
        return False

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


    @staticmethod
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
