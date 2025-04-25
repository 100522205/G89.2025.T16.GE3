"""attributes module"""
import re

from uc3m_money.account_management_exception import AccountManagementException


class Attribute:
    """super class for validations"""
    def __init__(self):
        self._attr_value = ""
        self._error_message = ""
        self._validation_pattern = r""

    def _validate(self, value):
        """general validation code"""
        myregex =re.compile(self._validation_pattern)
        res = myregex.fullmatch(value)
        if not res:
            raise AccountManagementException(self._error_message)
        return value

    @property
    def value(self):
        """value property"""
        return self._attr_value

    @value.setter
    def value(self, attr_value):
        """value setter"""
        self._attr_value = attr_value

    @property
    def message(self):
        """message property"""
        return self._error_message

    @message.setter
    def message(self, error_message):
        self._error_message = error_message

    @property
    def pattern(self):
        """message setter"""
        return self._validation_pattern

    @pattern.setter
    def pattern(self, validation_pattern):
        self._validation_pattern = validation_pattern
