from enum import Enum


class CardType(Enum):
    CHARACTER = 'CHARACTER'
    PLACE = 'PLACE'
    WEAPON = 'WEAPON'


class Card:
    def __init__(self, value, category: CardType):
        """
        :param value: String description of the card
        :param category: CardType object to distinguish between characters, weapons, and rooms
        """
        self.value = value
        self.category = category

    def get_value(self):
        """
        :return: String value of the card
        """
        return self.value

    def get_category(self):
        """
        :return: CardType
        """
        return self.category

    def to_string(self):
        """
        Prints the value out
        """
        print(self.value)
