"""Account manager module """
from datetime import datetime, timezone
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.storage.json_store import JsonStore

from uc3m_money.transfer_request import TransferRequest
from uc3m_money.account_deposit import AccountDeposit
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

        all_transfers = TransferRequestJsonStore()
        all_transfers.add_item(my_request)
        return my_request.transfer_code

        return my_request.transfer_code

    def deposit_into_account(self, input_file:str)->str:
        """manages the deposits received for accounts"""
        deposit_amount, deposit_iban = JsonStore.load_deposit(input_file)

        Iban(deposit_iban)
        DepositAmount(deposit_amount)

        deposit_obj = AccountDeposit(to_iban=deposit_iban,
                                     deposit_amount=deposit_amount)

        JsonStore.save_deposit(deposit_obj)

        return deposit_obj.deposit_signature

    def calculate_balance(self, iban:str)->bool:
        """calculate the balance for a given iban"""
        Iban(iban)
        transfer_load = JsonStore.read_transactions_file()
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

        JsonStore.save_balance(last_balance)
        return True
