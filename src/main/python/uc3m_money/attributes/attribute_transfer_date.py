from uc3m_money.attributes.attributes import Attribute
from uc3m_money.account_management_exception import AccountManagementException
from datetime import datetime, timezone


class TransferDate(Attribute):
    def __init__(self, attr_value):
        self._error_message = "Invalid date format"
        self._validation_pattern = r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$"
        self._attr_value =self._validate(attr_value)

    def _validate(self, attr_value:str)->str:
        """validates the arrival date format  using regex"""
        super()._validate(attr_value)

        try:
            my_date = datetime.strptime(attr_value, "%d/%m/%Y").date()
        except ValueError as exception:
            raise AccountManagementException(self._error_message) from exception

        if my_date < datetime.now(timezone.utc).date():
            raise AccountManagementException("Transfer date must be today or later.")

        if my_date.year < 2025 or my_date.year > 2050:
            raise AccountManagementException(self._error_message)

        return attr_value
