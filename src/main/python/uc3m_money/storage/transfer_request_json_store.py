from uc3m_money.storage.json_store import JsonStore
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.account_management_config import TRANSFERS_STORE_FILE


class TransferRequestJsonStore(JsonStore):
    _file_name = TRANSFERS_STORE_FILE

    def add_item(self, item):
        transfer_request_found = self.find_item(key="transfer_code", value=item.transfer_code)
        if transfer_request_found:
            raise AccountManagementException("Duplicated transfer in transfer list")
        super().add_item(item.to_json)
