from uc3m_money.attributes.attributes import Attribute
from uc3m_money.account_management_exception import AccountManagementException


class TransferAmount(Attribute):
    def __init__(self, attr_value):
        self._error_message = "Invalid transfer amount"
        self._validation_pattern = r"^(?:\d+)(?:\.\d{1,2})?$"
        self._attr_value =self._validate(attr_value)

    def _validate(self, attr_value:float):
        """method for validating transfer amount"""
        super()._validate(attr_value)

        float_amount = float(attr_value)
        if float_amount < 10 or float_amount > 10000:
            raise AccountManagementException("Invalid transfer amount")

        return attr_value
