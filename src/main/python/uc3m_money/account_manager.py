"""Account manager module """
import re
import json
from datetime import datetime, timezone
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.account_management_config import (TRANSFERS_STORE_FILE,
                                        DEPOSITS_STORE_FILE,
                                        TRANSACTIONS_STORE_FILE,
                                        BALANCES_STORE_FILE)

from uc3m_money.transfer_request import TransferRequest
from uc3m_money.account_deposit import AccountDeposit


class AccountManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_iban(iban_code: str):
        """
    Calcula el dígito de control de un IBAN español.

    Args:
        iban_code (str): El IBAN sin los dos últimos dígitos (dígito de control).

    Returns:
        str: El dígito de control calculado.
        """
        pattern = re.compile(r"^ES[0-9]{22}")
        result = pattern.fullmatch(iban_code)
        if not result:
            raise AccountManagementException("Invalid IBAN format")
        iban = iban_code
        original_code = iban[2:4]
        #replacing the control
        iban = iban[:2] + "00" + iban[4:]
        iban = iban[4:] + iban[:4]


        # Convertir el IBAN en una cadena numérica, reemplazando letras por números
        iban = (iban.replace('A', '10').replace('B', '11').
                replace('C', '12').replace('D', '13').replace('E', '14').
                replace('F', '15'))
        iban = (iban.replace('G', '16').replace('H', '17').
                replace('I', '18').replace('J', '19').replace('K', '20').
                replace('L', '21'))
        iban = (iban.replace('M', '22').replace('N', '23').
                replace('O', '24').replace('P', '25').replace('Q', '26').
                replace('R', '27'))
        iban = (iban.replace('S', '28').replace('T', '29').replace('U', '30').
                replace('V', '31').replace('W', '32').replace('X', '33'))
        iban = iban.replace('Y', '34').replace('Z', '35')

        # Mover los cuatro primeros caracteres al final

        # Convertir la cadena en un número entero
        int_iban = int(iban)

        # Calcular el módulo 97
        module = int_iban % 97

        # Calcular el dígito de control (97 menos el módulo)
        control_digit = 98 - module

        if int(original_code) != control_digit:
            #print(dc)
            raise AccountManagementException("Invalid IBAN control digit")

        return iban_code

    def validate_concept(self, concept: str):
        """regular expression for checking the minimum and maximum length as well as
        the allowed characters and spaces restrictions
        there are other ways to check this"""
        myregex = re.compile(r"^(?=^.{10,30}$)([a-zA-Z]+(\s[a-zA-Z]+)+)$")

        result = myregex.fullmatch(concept)
        if not result:
            raise AccountManagementException ("Invalid concept format")

    def validate_transfer_date(self, transfer_name):
        """validates the arrival date format  using regex"""
        pattern = re.compile(r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$")
        result = pattern.fullmatch(transfer_name)
        if not result:
            raise AccountManagementException("Invalid date format")

        try:
            my_date = datetime.strptime(transfer_name, "%d/%m/%Y").date()
        except ValueError as exception:
            raise AccountManagementException("Invalid date format") from exception

        if my_date < datetime.now(timezone.utc).date():
            raise AccountManagementException("Transfer date must be today or later.")

        if my_date.year < 2025 or my_date.year > 2050:
            raise AccountManagementException("Invalid date format")
        return transfer_name
    #pylint: disable=too-many-arguments
    def transfer_request(self, from_iban: str,
                         to_iban: str,
                         concept: str,
                         transfer_type: str,
                         date: str,
                         amount: float)->str:
        """first method: receives transfer info and
        stores it into a file"""
        self.validate_iban(from_iban)
        self.validate_iban(to_iban)
        self.validate_concept(concept)
        pattern = re.compile(r"(ORDINARY|INMEDIATE|URGENT)")
        result = pattern.fullmatch(transfer_type)
        if not result:
            raise AccountManagementException("Invalid transfer type")
        self.validate_transfer_date(date)



        try:
            float_amount  = float(amount)
        except ValueError as exception:
            raise AccountManagementException("Invalid transfer amount") from exception

        amount_str = str(float_amount)
        if '.' in amount_str:
            decimals = len(amount_str.split('.')[1])
            if decimals > 2:
                raise AccountManagementException("Invalid transfer amount")

        if float_amount < 10 or float_amount > 10000:
            raise AccountManagementException("Invalid transfer amount")

        my_request = TransferRequest(from_iban=from_iban,
                                     to_iban=to_iban,
                                     transfer_concept=concept,
                                     transfer_type=transfer_type,
                                     transfer_date=date,
                                     transfer_amount=amount)

        try:
            with open(TRANSFERS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                transfer_load = json.load(file)
        except FileNotFoundError:
            transfer_load = []
        except json.JSONDecodeError as exception:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from exception

        for transfer_instance in transfer_load:
            if (transfer_instance["from_iban"] == my_request.from_iban and
                    transfer_instance["to_iban"] == my_request.to_iban and
                    transfer_instance["transfer_date"] == my_request.transfer_date and
                    transfer_instance["transfer_amount"] == my_request.transfer_amount and
                    transfer_instance["transfer_concept"] == my_request.transfer_concept and
                    transfer_instance["transfer_type"] == my_request.transfer_type):
                raise AccountManagementException("Duplicated transfer in transfer list")

        transfer_load.append(my_request.to_json())

        try:
            with open(TRANSFERS_STORE_FILE, "w", encoding="utf-8", newline="") as file:
                json.dump(transfer_load, file, indent=2)
        except FileNotFoundError as exception:
            raise AccountManagementException("Wrong file  or file path") from exception
        except json.JSONDecodeError as exception:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from exception

        return my_request.transfer_code

    def deposit_into_account(self, input_file:str)->str:
        """manages the deposits received for accounts"""
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


        deposit_iban = self.validate_iban(deposit_iban)
        myregex = re.compile(r"^EUR [0-9]{4}\.[0-9]{2}")
        result = myregex.fullmatch(deposit_amount)
        if not result:
            raise AccountManagementException("Error - Invalid deposit amount")

        deposit_account_float = float(deposit_amount[4:])
        if deposit_account_float == 0:
            raise AccountManagementException("Error - Deposit must be greater than 0")

        deposit_obj = AccountDeposit(to_iban=deposit_iban,
                                     deposit_amount=deposit_account_float)

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

        return deposit_obj.deposit_signature


    def read_transactions_file(self):
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


    def calculate_balance(self, iban:str)->bool:
        """calculate the balance for a given iban"""
        iban = self.validate_iban(iban)
        transfer_load = self.read_transactions_file()
        iban_found = False
        balance_sum = 0
        for transaction in transfer_load:
            #print(transaction["IBAN"] + " - " + iban)
            if transaction["IBAN"] == iban:
                balance_sum += float(transaction["amount"])
                iban_found = True
        if not iban_found:
            raise AccountManagementException("IBAN not found")

        last_balance = {"IBAN": iban,
                        "time": datetime.timestamp(datetime.now(timezone.utc)),
                        "BALANCE": balance_sum}

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
        return True
