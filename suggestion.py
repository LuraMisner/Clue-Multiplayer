
class Suggestion:
    def __init__(self, player, character, weapon, room):
        self.player = player
        self.character = character
        self.weapon = weapon
        self.room = room
        self.solved = False
        self.result = None

    def get_player(self) -> str:
        """
        :return: String representing player who called the suggestion
        """
        return self.player

    def get_character(self) -> str:
        """
        :return: String representing the murder suspect
        """
        return self.character

    def get_weapon(self) -> str:
        """
        :return: String representing the murder weapon
        """
        return self.weapon

    def get_room(self) -> str:
        """
        :return: String representing the murder location
        """
        return self.room

    def get_solved(self) -> bool:
        """
        :return: Boolean of whether this suggestion has been answered
        """
        return self.solved

    def get_result(self) -> str:
        """
        :return: String representing the answer to the suggestion
        """
        return self.result

    def solve(self):
        """
        Flags suggestion as solved
        """
        self.solved = True

    def set_result(self, data):
        """
        :param data: String representing the answer to the suggestion
        """
        self.solve()
        self.result = data
