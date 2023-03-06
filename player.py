from characters import Characters
import constants


class Player:
    def __init__(self, character: Characters):
        """
        Initializes items unique to each player (cards, notes, position, and character)
        :param character: Character object
        """
        self.cards = []
        self.character = character
        # Index 0: Characters, Index 1: Weapons, Index 2: Places
        self.notes = [[], [], []]
        self.position = constants.START_POSITIONS[character.value]
        self.disqualified = False

    def add_note(self, card):
        """
        Adds information to our players notes
        :param card: Card object
        :return: None
        """
        if card in ['Colonel Mustard', 'Professor Plum', 'Reverend Green', 'Mr.Peacock', 'Miss Scarlet', 'Mrs.White']:
            self.notes[0].append(card)
        elif card in ['Knife', 'Candle stick', 'Revolver', 'Rope', 'Lead pipe', 'Wrench']:
            self.notes[1].append(card)
        elif card in ['Hall', 'Lounge', 'Dining Room', 'Kitchen', 'Ballroom', 'Conservatory',
                      'Billiard Room', 'Library', 'Study']:
            self.notes[2].append(card)
        else:
            print("Error adding to notes: Unidentified")

    def add_card(self, card):
        """
        Adds a card to our deck (and appends it to notes because its information the player knows)
        :param card: Card object
        :return: None
        """
        self.cards.append(card)
        self.add_note(card.value)

    def set_position(self, new_position):
        """
        :param new_position: Integer, space ID of new position
        """
        self.position = new_position

    def get_cards(self):
        """
        :return: Array of Card objects
        """
        return self.cards

    def get_position(self):
        """
        :return: Integer of space ID
        """
        return self.position

    def get_character(self):
        """
        :return: Character object
        """
        return self.character

    def get_notes(self):
        """
        :return: Array of (3) arrays of strings
        """
        return self.notes

    def print_notes(self):
        """
        Prints notes to terminal
        """

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

    def disqualify(self):
        self.disqualified = True

    def get_disqualified(self):
        return self.disqualified
