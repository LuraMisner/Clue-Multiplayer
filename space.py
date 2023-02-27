from roomtype import RoomType


class Space:
    def __init__(self, identifier: int, occupied: bool, room: RoomType):
        self.id = identifier
        self.occupied = occupied
        self.room = room

    def get_id(self):
        return self.id

    def get_occupied(self):
        return self.occupied

    def get_room(self):
        return self.room

    def set_occupied(self, status):
        self.occupied = status

    def to_string(self):
        print(str(self.id) + " " + str(self.room.value))
