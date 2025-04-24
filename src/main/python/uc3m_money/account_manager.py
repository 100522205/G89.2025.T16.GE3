"""Account manager module """
from datetime import datetime, timezone
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.storage.deposit_json_store import DepositJsonStore
from uc3m_money.storage.account_balance_json_store import AccountBalanceJsonStore
from uc3m_money.storage.json_store import JsonStore

from uc3m_money.transfer_request import TransferRequest
from uc3m_money.account_deposit import AccountDeposit
from uc3m_money.account_balance import AccountBalance
from uc3m_money.attributes.attribute_iban import Iban
from uc3m_money.attributes.attribute_concept import Concept
from uc3m_money.attributes.attribute_transfer_date import TransferDate
from uc3m_money.attributes.attribute_transfer_type import TransferType
from uc3m_money.attributes.attribute_transfer_amount import TransferAmount
from uc3m_money.attributes.attribute_deposit_amount import DepositAmount

from uc3m_money.storage.transfer_request_json_store import TransferRequestJsonStore


class AccountManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    #pylint: disable=too-many-arguments
    def transfer_request(self, from_iban: str,
                         to_iban: str,
                         concept: str,
                         transfer_type: str,
                         date: str,
                         amount: float)->str:
        """first method: receives transfer info and
        stores it into a file"""
        Iban(from_iban)
        Iban(to_iban)
        Concept(concept)
        TransferType(transfer_type)
        TransferDate(date)
        TransferAmount(str(amount))

        my_request = TransferRequest(from_iban=from_iban,
                                     to_iban=to_iban,
                                     transfer_concept=concept,
                                     transfer_type=transfer_type,
                                     transfer_date=date,
                                     transfer_amount=amount)

        at = TransferRequestJsonStore()
        at.save_transfer_request(my_request)

        return my_request.transfer_code

    def deposit_into_account(self, input_file:str)->str:
        """manages the deposits received for accounts"""
        deposit_obj = AccountDeposit.create_new_deposit_from_file(input_file)

        #Check if iban is correct
        Iban(deposit_obj.to_iban)
        #Check if amount is correct
        DepositAmount(deposit_obj.deposit_amount)
        #Add the deposit to the json file
        DepositJsonStore().store_deposit(deposit_obj)
        #Return the deposit signature
        return deposit_obj.deposit_signature

    def calculate_balance(self, iban:str)->bool:
        """calculate the balance for a given iban"""
        balance_obj = AccountBalance.create_from_transactions(iban)

        store = AccountBalanceJsonStore()
        store._data_list.append(balance_obj.to_json())
        store.save_list_to_file()

        return True
