
class Envelope:
    def __init__(self, character, weapon, location):
        self.character = character
        self.weapon = weapon
        self.location = location

    def check_guess(self, character, weapon, location):
        return character == self.character.get_value() and \
            weapon == self.weapon.get_value() and location == self.location.get_value()
