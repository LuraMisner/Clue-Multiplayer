from card import CardType
from characters import Characters


class Player:
    def __init__(self, character: Characters, start):
        self.cards = []
        self.character = character
        # Index 0: Characters, Index 1: Weapons, Index 2: Places
        self.notes = [[], [], []]
        self.position = start

    def add_note(self, card):
        value = card.get_value()
        category = card.get_category()
        if category == CardType.CHARACTER:
            self.notes[0].append(value)
        elif category == CardType.WEAPON:
            self.notes[1].append(value)
        elif category == CardType.PLACE:
            self.notes[2].append(value)
        else:
            print("Error adding to notes: Unidentified")

    def add_card(self, card):
        self.cards.append(card)
        self.add_note(card)

    def set_position(self, new_position):
        self.position = new_position

    def get_cards(self):
        return self.cards

    def get_position(self):
        return self.position

    def get_character(self):
        return self.character

    def print_notes(self):
        print("------------- NOTES -----------------")
        print("It can't be these characters:")
        for character in self.notes[0]:
            print(character)
        print()

        print("It can't be these weapons:")
        for weapon in self.notes[1]:
            print(weapon)
        print()

        print("It can't be these locations:")
        for location in self.notes[2]:
            print(location)
        print("----------- END NOTES ---------------")
