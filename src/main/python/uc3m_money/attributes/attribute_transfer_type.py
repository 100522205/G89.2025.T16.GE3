"""attribute_transfer_type module"""
from uc3m_money.attributes.attributes import Attribute


class TransferType(Attribute):
    """transfer type validation module"""
    def __init__(self, attr_value):
        super().__init__()
        self._error_message = "Invalid transfer type"
        self._validation_pattern = r"(ORDINARY|INMEDIATE|URGENT)"
        self._attr_value =self._validate(attr_value)

    #pylint:disable=arguments-renamed
    # pylint:disable=useless-parent-delegation
    def _validate(self, attr_value:str)->str:
        """method for validating transfer type"""
        return super()._validate(attr_value)
