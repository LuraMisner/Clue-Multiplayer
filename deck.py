import random
from card import Card, CardType


class Deck:
    def __init__(self):
        self.deck = []

        # Characters
        self.deck.append(Card('Colonel Mustard', CardType.CHARACTER))
        self.deck.append(Card('Professor Plum', CardType.CHARACTER))
        self.deck.append(Card('Reverend Green', CardType.CHARACTER))
        self.deck.append(Card('Mr.Peacock', CardType.CHARACTER))
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
        random.shuffle(self.deck)

    def to_string(self):
        for card in self.deck:
            card.to_string()
