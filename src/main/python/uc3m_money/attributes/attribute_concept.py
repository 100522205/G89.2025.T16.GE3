from uc3m_money.attributes.attributes import Attribute


class Concept(Attribute):
    def __init__(self, attr_value):
        self._error_message = "Invalid concept format"
        self._validation_pattern = r"^(?=^.{10,30}$)([a-zA-Z]+(\s[a-zA-Z]+)+)$"
        self._attr_value =self._validate(attr_value)

    def _validate(self, attr_value:str)->str:
        """regular expression for checking the minimum and maximum length as well as
        the allowed characters and spaces restrictions
        there are other ways to check this"""
        return  super()._validate(attr_value)
