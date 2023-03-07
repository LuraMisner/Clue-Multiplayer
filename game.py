from characters import Characters
from deck import Deck
from envelope import Envelope
from player import Player
from suggestion import Suggestion
import random


class Game:
    def __init__(self, gid):
        self.id = gid
        self.turn = 0
        self.won = False
        self.who_won = None
        self.split = False

        self.deck = Deck()
        self.envelop = self.create_envelope()
        self.deck.shuffle()

        self.available_characters = [Characters.COLONEL_MUSTARD, Characters.PROFESSOR_PLUM, Characters.MR_PEACOCK,
                                     Characters.MRS_WHITE, Characters.REVEREND_GREEN, Characters.MISS_SCARLET]

        self.players = []
        self.player_count = 0

        self.pending_suggestion = False
        self.waiting_on = None
        self.suggestions = []

    def create_envelope(self) -> Envelope:
        """
        Randomly selects three cards (one of each type) from the deck and creates the envelope
        :return: Envelope object
        """
        random_character = self.deck.deck.pop(random.randint(0, 5))
        random_weapon = self.deck.deck.pop(random.randint(5, 10))
        random_location = self.deck.deck.pop(random.randint(10, len(self.deck.deck) - 1))
        return Envelope(random_character, random_weapon, random_location)

    def split_cards(self):
        """
        Splits the deck of cards between the current players
        :return: None
        """
        self.split = True

        while len(self.deck.deck) > 0:
            for player in self.players:
                if len(self.deck.deck) > 0:
                    player.add_card(self.deck.deck.pop())

    def add_player(self, player) -> bool:
        """
        Creates the player objects
        :param player: String of a characters name
        :return: Boolean of whether creating the player was successful
        """
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
            self.players.append(Player(character))
            self.player_count += 1
            self.available_characters.remove(character)
            return True

        print("Invalid Character Selection")
        return False

    def make_accusation(self, player, character, weapon, room):
        """
        :param player: String representing the players name
        :param character: String representing characters name
        :param weapon: String representing weapons name
        :param room: String representing a room
        """

        # If they are right, then they won the game
        if self.envelop.check_guess(character, weapon, room):
            self.won = True
            self.who_won = player
        else:
            # If a wrong suggestion is made, then they must be disqualified
            for p in self.players:
                if p.get_character().value == player:
                    p.disqualify()

            # Check if all players have been disqualified, if so, then they lose
            disqualified = []
            for p in self.players:
                disqualified.append(p.get_disqualified())

            if all(disqualified):
                self.won = True

    def get_id(self) -> int:
        """
        :return: Integer of game ID
        """
        return self.id

    def get_split(self) -> bool:
        """
        :return: Boolean representing if cards have been distributed to the players
        """
        return self.split

    def get_player_count(self) -> int:
        """
        :return: Integer count of players
        """
        return self.player_count

    def get_won(self) -> bool:
        """
        :return: Boolean of whether the game has been won
        """
        return self.won

    def whos_turn(self):
        """
        Calculates which players turn it is
        :return: Player object
        """
        return self.players[self.turn % self.player_count]

    def get_turn(self):
        """
        :return: Integer representing how many turns have happened in the game
        """
        return self.turn

    def increment_turn(self):
        self.turn += 1

    def get_player_location(self, character):
        """
        :param character: String of a character name
        :return: Integer space ID of that players position
        """
        for player in self.players:
            if player.get_character().value == character:
                return player.get_position()

    def get_player_cards(self, character):
        """
        :param character: String of a character name
        :return: Array of Card objects
        """
        for player in self.players:
            if player.get_character().value == character:
                return player.get_cards()

    def get_player_notes(self, character):
        """
        :param character: String of a character name
        :return: Array of (3) arrays of strings
        """
        for player in self.players:
            if player.get_character().value == character:
                return player.get_notes()

    def get_all_player_locations(self):
        """
        :return: Dictionary mapping of { characters name (str) -> characters position (int) }
        """
        d = {}
        for player in self.players:
            d[player.get_character().value] = player.get_position()

        return d

    def update_player_position(self, name, position):
        """
        Updates a players position
        :param name: Name of the character
        :param position: New position
        :return: None
        """
        for player in self.players:
            if player.get_character().value == name:
                player.set_position(position)

    def make_suggestion(self, player, character, weapon, room):
        if not self.pending_suggestion:
            self.suggestions.append(Suggestion(player, character, weapon, room))

            for pl in self.players:
                if pl.get_character().value == player:
                    self.waiting_on = pl
                    self.next_player()

    def get_pending_suggestion(self):
        self.check_suggestion_status()
        return self.pending_suggestion

    def get_waiting_on(self):
        return self.waiting_on

    def get_last_suggestion(self):
        if len(self.suggestions) > 0:
            return self.suggestions[len(self.suggestions) - 1]

    def check_suggestion_status(self):
        if len(self.suggestions) > 0:
            if self.get_last_suggestion().get_solved():
                self.pending_suggestion = False
            else:
                self.pending_suggestion = True

    def next_player(self):
        current = self.waiting_on
        suggestion_player = self.get_last_suggestion().get_player()

        index = self.players.index(current)
        self.waiting_on = self.players[((index + 1) % len(self.players))]

        # Check if we made it around the table without getting solved
        if self.waiting_on.get_character().value == suggestion_player:
            self.get_last_suggestion().set_result('No one could disprove')
            self.check_suggestion_status()

    def answer_suggestion(self, data):
        self.get_last_suggestion().set_result(data)

    def get_suggestion_response(self):
        return self.get_last_suggestion().get_result()

    def add_note(self, character, note):
        for player in self.players:
            if player.get_character().value == character:
                player.add_note(note)

    def get_player_disqualification(self, character):
        for player in self.players:
            if player.get_character().value == character:
                return player.get_disqualified()

    def get_winner(self):
        if self.won:
            return self.who_won

    def early_quit(self, player):
        quitter = None
        index = 0
        for ind, p in enumerate(self.players):
            if p.get_character().value == player:
                quitter = p
                index = ind

        if quitter:
            # Remove them from the list of players, and give other players their cards
            self.players.pop(index)
            self.player_count -= 1

            players_cards = quitter.get_cards()
            i = 0
            while players_cards:
                self.players[i % len(self.players)].add_card(players_cards.pop())
                i += 1
