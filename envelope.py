
class Envelope:
    def __init__(self, character, weapon, location):
        """
        Takes three cards (one of each type) at random to represent the murder mystery being solved
        :param character: Character Card
        :param weapon: Weapon Card
        :param location: Room Card
        """
        self.character = character
        self.weapon = weapon
        self.location = location

    def check_guess(self, character, weapon, location) -> bool:
        """
        Checks a given guess against the actual items in the envelope
        :param character: String of a character card value
        :param weapon: String of a weapon card value
        :param location: String of a room value
        :return: Boolean of if the guess was correct
        """
        return character == self.character.get_value() and \
            weapon == self.weapon.get_value() and location == self.location.get_value()
