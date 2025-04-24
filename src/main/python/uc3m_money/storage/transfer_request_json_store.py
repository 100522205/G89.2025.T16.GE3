from uc3m_money.storage.json_store import JsonStore
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.account_management_config import TRANSFERS_STORE_FILE

class TransferRequestJsonStore(JsonStore):
    def __init__(self):
        super().__init__()
        self._file_name = TRANSFERS_STORE_FILE

    def save_transfer_request(self, my_request):
        self.load_list_from_file(fnf_error=False)
        if self.find_item(key="transfer_code", value=my_request.transfer_code):
            raise AccountManagementException("Duplicated transfer in transfer list")
        self.add_item(my_request)
        self.save_list_to_file()
