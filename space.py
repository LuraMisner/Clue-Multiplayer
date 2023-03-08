from roomtype import RoomType


class Space:
    def __init__(self, identifier: int, occupied: bool, room: RoomType):
        self.id = identifier
        self.occupied = occupied
        self.room = room

    def get_id(self) -> int:
        """
        :return: Integer representing the id of the space
        """
        return self.id

    def get_occupied(self) -> bool:
        """
        :return: Boolean whether this space is occupied
        """
        return self.occupied

    def get_room(self) -> RoomType:
        """
        :return: RoomType enum representing the type of room
        """
        return self.room

    def set_occupied(self, status):
        """
        :param status: Boolean
        """
        self.occupied = status

    def to_string(self):
        """
        Prints the space out to console
        """
        print(str(self.id) + " " + str(self.room.value))
