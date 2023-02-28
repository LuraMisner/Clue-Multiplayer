from characters import Characters
from deck import Deck
from envelope import Envelope
from player import Player
import random
import constants


class Game:
    def __init__(self, gid):
        self.id = gid
        self.turn = 0
        self.won = False
        self.split = False

        self.deck = Deck()
        self.envelop = self.create_envelope()
        self.deck.shuffle()

        self.available_characters = [Characters.COLONEL_MUSTARD, Characters.PROFESSOR_PLUM, Characters.MR_PEACOCK,
                                     Characters.MRS_WHITE, Characters.REVEREND_GREEN, Characters.MISS_SCARLET]

        self.players = []
        self.player_count = 0

    def create_envelope(self) -> Envelope:
        random_character = self.deck.deck.pop(random.randint(0, 5))
        random_weapon = self.deck.deck.pop(random.randint(5, 10))
        random_location = self.deck.deck.pop(random.randint(10, len(self.deck.deck) - 1))
        return Envelope(random_character, random_weapon, random_location)

    def split_cards(self):
        self.split = True

        while len(self.deck.deck) > 0:
            for player in self.players:
                if len(self.deck.deck) > 0:
                    player.add_card(self.deck.deck.pop())

    def add_player(self, player) -> bool:
        character = None

        if player == 'Colonel Mustard':
            character = Characters.COLONEL_MUSTARD
        elif player == 'Miss Scarlet':
            character = Characters.MISS_SCARLET
        elif player == 'Mrs.White':
            character = Characters.MRS_WHITE
        elif player == 'Mr.Peacock':
            character = Characters.MR_PEACOCK
        elif player == 'Professor Plum':
            character = Characters.PROFESSOR_PLUM
        elif player == 'Reverend Green':
            character = Characters.REVEREND_GREEN

        if character:
            self.players.append(Player(character, constants.START_POSITIONS[player]))
            self.player_count += 1
            self.available_characters.remove(character)
            return True

        print("Invalid Character Selection")
        return False

    def win_condition(self, character, weapon, room):
        if self.envelop.check_guess(character, weapon, room):
            self.won = True

    def get_id(self):
        return self.id

    def get_split(self):
        return self.split

    def get_player_count(self):
        return self.player_count

    def get_player_location(self, character):
        for player in self.players:
            if player.get_character().value == character:
                return player.get_position()

    def get_player_cards(self, character):
        for player in self.players:
            if player.get_character().value == character:
                return player.get_cards()

    def get_player_notes(self, character):
        for player in self.players:
            if player.get_character().value == character:
                return player.get_notes()

    def get_all_player_locations(self):
        d = {}
        for player in self.players:
            d[player.get_character().value] = player.get_position()

        return d

    def get_won(self):
        return self.won

    def whos_turn(self):
        return self.players[self.turn % self.player_count]

    def increment_turn(self):
        self.turn += 1
