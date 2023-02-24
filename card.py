from enum import Enum


class CardType(Enum):
    CHARACTER = 'CHARACTER'
    PLACE = 'PLACE'
    WEAPON = 'WEAPON'


class Card:
    def __init__(self, value, category: CardType):
        self.value = value
        self.category = category

    def get_value(self):
        return self.value

    def get_category(self):
        return self.category

    def to_string(self):
        print(self.value)
