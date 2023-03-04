
class Suggestion:
    def __init__(self, player, character, weapon, room):
        self.player = player
        self.character = character
        self.weapon = weapon
        self.room = room
        self.solved = False
        self.result = None

    def get_player(self):
        return self.player

    def get_character(self):
        return self.character

    def get_weapon(self):
        return self.weapon

    def get_room(self):
        return self.room

    def get_solved(self):
        return self.solved

    def get_result(self):
        return self.result

    def solve(self):
        self.solved = True

    def set_result(self, data):
        self.solve()
        self.result = data
