import random
from card import Card, CardType


class Deck:
    def __init__(self):
        """
        Constructs the deck with the 21 unique cards
        """
        self.deck = []

        # Characters
        self.deck.append(Card('Colonel Mustard', CardType.CHARACTER))
        self.deck.append(Card('Professor Plum', CardType.CHARACTER))
        self.deck.append(Card('Reverend Green', CardType.CHARACTER))
        self.deck.append(Card('Mrs.Peacock', CardType.CHARACTER))
        self.deck.append(Card('Miss Scarlet', CardType.CHARACTER))
        self.deck.append(Card('Mrs.White', CardType.CHARACTER))

        # Weapons
        self.deck.append(Card('Knife', CardType.WEAPON))
        self.deck.append(Card('Candle stick', CardType.WEAPON))
        self.deck.append(Card('Revolver', CardType.WEAPON))
        self.deck.append(Card('Rope', CardType.WEAPON))
        self.deck.append(Card('Lead pipe', CardType.WEAPON))
        self.deck.append(Card('Wrench', CardType.WEAPON))

        # Locations
        self.deck.append(Card('Hall', CardType.PLACE))
        self.deck.append(Card('Lounge', CardType.PLACE))
        self.deck.append(Card('Dining Room', CardType.PLACE))
        self.deck.append(Card('Kitchen', CardType.PLACE))
        self.deck.append(Card('Ballroom', CardType.PLACE))
        self.deck.append(Card('Conservatory', CardType.PLACE))
        self.deck.append(Card('Billiard Room', CardType.PLACE))
        self.deck.append(Card('Library', CardType.PLACE))
        self.deck.append(Card('Study', CardType.PLACE))

    def shuffle(self):
        """
        Shuffles the deck
        """
        random.shuffle(self.deck)

    def to_string(self):
        """
        Prints the deck card by card
        """
        for card in self.deck:
            card.to_string()

    @staticmethod
    def all_values() -> [[str]]:
        """
        :return: Array of arrays of strings for all values in the deck
        """
        return [['Colonel Mustard', 'Professor Plum', 'Reverend Green', 'Mrs.Peacock', 'Miss Scarlet', 'Mrs.White'],
                ['Knife', 'Candle stick', 'Revolver', 'Rope', 'Lead pipe', 'Wrench'], ['Hall', 'Lounge', 'Dining Room',
                'Kitchen', 'Ballroom', 'Conservatory', 'Billiard Room', 'Library', 'Study']]
