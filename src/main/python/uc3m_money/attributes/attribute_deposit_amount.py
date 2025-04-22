from uc3m_money.attributes.attributes import Attribute
from uc3m_money.account_management_exception import AccountManagementException


class DepositAmount(Attribute):
    def __init__(self, attr_value):
        self._error_message = "Error - Invalid deposit amount"
        self._validation_pattern = r"^EUR [0-9]{4}\.[0-9]{2}"
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value: str)->float:
        """method for validating deposit amount"""
        super()._validate(attr_value)

        attr_value = float(attr_value[4:])
        if attr_value == 0:
            raise AccountManagementException("Error - Deposit must be greater than 0")

        return attr_value
