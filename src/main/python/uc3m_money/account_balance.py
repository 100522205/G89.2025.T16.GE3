from datetime import datetime, timezone
from uc3m_money.storage.transactions_json_store import TransactionsJsonStore
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.attributes.attribute_iban import Iban

class AccountBalance:
    def __init__(self, iban, balance, timestamp):
        self._iban = iban
        self._balance = balance
        self._timestamp = timestamp

    def to_json(self):
        return {
            "IBAN": self._iban,
            "time": self._timestamp,
            "BALANCE": self._balance
        }

    @classmethod
    def create_from_transactions(cls, iban):
        Iban(iban)

        store = TransactionsJsonStore()
        transactions = store.load_list_from_file(fnf_error=True)

        balance_sum = 0
        iban_found = False
        for transaction in transactions:
            if transaction["IBAN"] == iban:
                balance_sum += float(transaction["amount"])
                iban_found = True

        if not iban_found:
            raise AccountManagementException("IBAN not found")

        timestamp = datetime.timestamp(datetime.now(timezone.utc))

        return cls(iban=iban, balance=balance_sum, timestamp=timestamp)