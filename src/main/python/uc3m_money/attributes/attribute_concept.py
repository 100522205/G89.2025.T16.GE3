"""module docstring for pylint errors"""
from uc3m_money.attributes.attributes import Attribute


class Concept(Attribute):
    """Class for validating Concept attribute"""
    def __init__(self, attr_value):
        super().__init__()
        self._error_message = "Invalid concept format"
        self._validation_pattern = r"^(?=^.{10,30}$)([a-zA-Z]+(\s[a-zA-Z]+)+)$"
        self._attr_value =self._validate(attr_value)

    # pylint:disable=useless-parent-delegation
    def _validate(self, value:str)->str:
        """regular expression for checking the minimum and maximum length as well as
        the allowed characters and spaces restrictions
        there are other ways to check this"""
        return  super()._validate(value)
