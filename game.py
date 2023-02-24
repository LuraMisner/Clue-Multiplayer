from board import Board
from characters import Characters
from deck import Deck
from envelope import Envelope
from player import Player


class Game:
    def __init__(self, gid):
        self.id = gid
        self.started = False

        self.deck = Deck()
        self.deck.shuffle()

        self.available_characters = [Characters.COLONEL_MUSTARD, Characters.PROFESSOR_PLUM, Characters.MR_PEACOCK,
                                     Characters.MRS_WHITE, Characters.REVEREND_GREEN, Characters.MISS_SCARLET]

        self.start_positions = {'Colonel Mustard': 408, 'Miss Scarlet': 583, 'Mr.Peacock': 167,
                                'Mrs.White': 9, 'Professor Plum': 479, 'Reverend Green': 14}
        self.players = []
        self.player_cards = []
        self.player_count = 0

        self.envelop = self.create_envelope()
        self.won = False

    def create_envelope(self) -> Envelope:
        pass

    def split_cards(self):
        pass

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
            self.players.append(Player(character, self.start_positions[player]))
            self.player_count += 1
            self.available_characters.remove(character)
            return True

        print("Invalid Character Selection")
        return False
