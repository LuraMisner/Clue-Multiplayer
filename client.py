import constants
import pygame
import random
import time
from board import Board
from characters import Characters
from deck import Deck
from picture import Picture
from network import Network
from roomtype import RoomType


class Client:
    def __init__(self, window):
        self.WIN = window
        self.n = Network()
        self.log = []
        self.player_positions = {}

        self.board = Board(self.WIN)
        self.cards = []
        self.notes = []
        self.character = None

        # Sprite groups for suggestions/accusations
        self.weapons_group = pygame.sprite.Group()
        self.rooms_group = pygame.sprite.Group()
        self.characters_group = pygame.sprite.Group()

    # noinspection PyTypeChecker
    def image_setups(self):
        """
        Initializes Pictures into their groups for the suggestions/accusations part
        """
        # Character button images
        self.characters_group.add(Picture(25, 100, 'images/character-buttons/colonel.png'))
        self.characters_group.add(Picture(175, 100, 'images/character-buttons/scarlet.png'))
        self.characters_group.add(Picture(325, 100, 'images/character-buttons/white.png'))
        self.characters_group.add(Picture(475, 100, 'images/character-buttons/green.png'))
        self.characters_group.add(Picture(25, 150, 'images/character-buttons/peacock.png'))
        self.characters_group.add(Picture(175, 150, 'images/character-buttons/plum.png'))

        # Weapon button images
        self.weapons_group.add(Picture(25, 250, 'images/weapon-buttons/knife.png'))
        self.weapons_group.add(Picture(175, 250, 'images/weapon-buttons/candle.png'))
        self.weapons_group.add(Picture(325, 250, 'images/weapon-buttons/revolver.png'))
        self.weapons_group.add(Picture(475, 250, 'images/weapon-buttons/rope.png'))
        self.weapons_group.add(Picture(25, 300, 'images/weapon-buttons/lead.png'))
        self.weapons_group.add(Picture(175, 300, 'images/weapon-buttons/wrench.png'))

        # Room button images
        self.rooms_group.add(Picture(25, 400, 'images/room-buttons/hall.png'))
        self.rooms_group.add(Picture(175, 400, 'images/room-buttons/lounge.png'))
        self.rooms_group.add(Picture(325, 400, 'images/room-buttons/dining.png'))
        self.rooms_group.add(Picture(475, 400, 'images/room-buttons/kitchen.png'))
        self.rooms_group.add(Picture(25, 450, 'images/room-buttons/ballroom.png'))
        self.rooms_group.add(Picture(175, 450, 'images/room-buttons/conservatory.png'))
        self.rooms_group.add(Picture(325, 450, 'images/room-buttons/billiards.png'))
        self.rooms_group.add(Picture(475, 450, 'images/room-buttons/library.png'))
        self.rooms_group.add(Picture(25, 500, 'images/room-buttons/study.png'))

    def ask_server(self, request):
        """
        Asks the server a request
        :return: Servers response
        """
        return self.n.send(request)

    def check_our_turn(self) -> bool:
        """
        Checks if it is the current players turn
        :return: Boolean
        """
        players_turn = self.ask_server('whos_turn')
        return players_turn.get_character() == self.character

    def check_pending_suggestion(self) -> bool:
        """
        Checks if there is a pending suggestion
        :return: Boolean
        """
        return self.ask_server('check_suggestion_status')

    def waiting_on_you(self) -> bool:
        """
        Checks if a suggestion is waiting on you to respond
        :return: Boolean
        """
        waiting = self.ask_server('waiting_on')
        if waiting:
            return self.ask_server('waiting_on').get_character() == self.character
        return False

    def update_cards(self):
        """
        Updates the clients cards
        """
        self.cards = self.ask_server('get_cards')

    def update_notes(self):
        """
        Updates the clients notes
        """
        self.notes = self.ask_server('get_notes')

    def update_log(self):
        """
        Updates the latest events in our log
        """
        self.log = self.ask_server('get_log')

    def update_player_positions(self):
        """
        Updates the dicitonary of player positions
        """
        self.player_positions = self.ask_server('get_all_positions')

    def update_our_position(self, position):
        """
        :param position: Integer position of where our character is
        """
        self.ask_server(f'update_position {position}')

    # This section contains functions that are used for the pre-game character selection screen
    def show_ready(self):
        """
        Creates a waiting screen for players in the game that have finished selecting their character
        """
        # Show how many players are ready
        self.WIN.fill(constants.BACKGROUND)
        num_ready = self.ask_server('num_ready')
        font = pygame.font.SysFont('freesansbold.ttf', 56)
        self.WIN.blit(font.render(f'Waiting on other players...', True, (0, 0, 0)), (275, 200))
        self.WIN.blit(font.render(f'{num_ready[1]} out of {num_ready[0]} players ready', True,
                                  constants.BLACK), (275, 275))

    def select_character(self):
        """
        Draws the character selection screen and allows the player to select what character they want to be
        """
        selection_made = False
        choice = None

        while not selection_made:
            available_characters = self.ask_server('character_selection')
            self.WIN.fill(constants.BACKGROUND)

            # How many players ready
            num_ready = self.ask_server('num_ready')
            self.draw_text(f'{num_ready[1]} out of {num_ready[0]} players ready', 26, constants.BLACK, 50, 50)

            # Fonts
            font2 = pygame.font.SysFont('freesansbold.ttf', 26)
            self.draw_text('Select a Character', 60, constants.BLACK, 300, 200)

            mapping = {}
            # Character options
            for i, ch in enumerate(available_characters):
                x = 75 + i * 150
                y = 300
                mapping[ch] = (x, y)

                if ch == Characters.COLONEL_MUSTARD:
                    color = constants.MUSTARD
                    text1 = 'Colonel'
                    text2 = 'Mustard'
                elif ch == Characters.MISS_SCARLET:
                    color = constants.SCARLET
                    text1 = 'Miss'
                    text2 = 'Scarlet'
                elif ch == Characters.MRS_PEACOCK:
                    color = constants.PEACOCK
                    text1 = 'Mrs.'
                    text2 = 'Peacock'
                elif ch == Characters.MRS_WHITE:
                    color = constants.WHITE
                    text1 = 'Mrs.'
                    text2 = 'White'
                elif ch == Characters.PROFESSOR_PLUM:
                    color = constants.PLUM
                    text1 = 'Professor'
                    text2 = 'Plum'
                else:
                    # Reverend Green
                    color = constants.GREEN
                    text1 = 'Reverend'
                    text2 = 'Green'

                self.draw_box(x, y, constants.CHARACTER_SELECTION_SIZE, constants.CHARACTER_SELECTION_SIZE, color)
                self.WIN.blit(font2.render(f'{text1}', True, constants.BLACK), (x + 25 - (1.5 * len(text1)), 330))
                self.WIN.blit(font2.render(f'{text2}', True, constants.BLACK), (x + 25 - (1.5 * len(text2)), 355))

            # Listen for clicks
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()

                    # Find out if the click maps to a character
                    for key in mapping.keys():
                        x, y = pos
                        x2, y2 = mapping[key]

                        if x2 < x < x2 + constants.CHARACTER_SELECTION_SIZE and \
                                y2 < y < y2 + constants.CHARACTER_SELECTION_SIZE:
                            choice = key

                    # Check if it is the confirmation button
                    if choice:
                        # Clicking confirmed
                        x, y = pos
                        if 425 <= x <= 425 + 125 and 600 <= y <= 600 + 65:
                            selection_made = True

            # Selection update
            self.draw_text('Character Selected: ', 32, constants.BLACK, 300, 500)

            # If a choice has been made, add a confirmation button to create the player
            if choice:
                self.draw_text(choice.value, 32, constants.BLACK, 550, 500)

            # Button to confirm selection (will confirm the selection made if choice != None
            self.draw_box(425, 600, 125, 65, constants.GREEN)
            self.draw_text('Confirm', 32, constants.BLACK, 442, 622)
            pygame.display.update()

        # Verify the choice is okay, if not then restart this process
        if self.ask_server(choice.value):
            self.character = choice
        else:
            self.select_character()

    # Section below handles screen visuals
    def draw_box(self, x, y, x_length, y_length, color):
        """
        Draws a box on the window
        :param x: Integer, x position of top left corner
        :param y: Integer, y position of top left corner
        :param x_length: Integer, length
        :param y_length: Integer, height
        :param color: (int, int, int), color of box
        """

        background = pygame.Rect(x, y, x_length, y_length)
        pygame.draw.rect(self.WIN, constants.BLACK, background)
        rect = pygame.Rect(x + 2, y + 2, x_length - 4, y_length - 4)
        pygame.draw.rect(self.WIN, color, rect)

    def draw_text(self, text, size, color, x, y):
        """
        Draws a text object on the window
        :param text: String, text being displayed
        :param size: Integer, size of the text
        :param color: (int, int, int), color of the text
        :param x: Integer, x position of top left corner
        :param y: Integer, y position of top left corner
        """
        font = pygame.font.SysFont('freesansbold.ttf', size)
        self.WIN.blit(font.render(text, True, color), (x, y))

    def draw_screen(self):
        """
        Used to call all the individual functions that make up the components of the GUI
        """

        current_turn = self.ask_server('whos_turn')
        self.board.draw_board()
        self.draw_players()

        self.update_cards()
        self.draw_cards()

        self.update_notes()
        self.draw_notes()

        self.draw_turn(current_turn)
        self.draw_log()

    def draw_log(self):
        """
        Log that displays recent actions of players to other players
        """
        self.update_log()

        if len(self.log) <= 6:
            these_logs = self.log
        else:
            these_logs = self.log[len(self.log) - 6:]

        self.draw_text('LOG', 22, constants.BLACK, 775, 550)
        self.draw_box(630, 565, constants.LOG_X, constants.LOG_Y, constants.LOG)

        for i, line in enumerate(these_logs):
            x = 636
            y = 573 + (i * 20)

            if len(line) <= 50:
                self.draw_text(line, 16, constants.WHITE, x, y)
            else:
                self.draw_text(line, 14, constants.WHITE, x, y)

    def draw_players(self):
        """
        Draws the player piece (circle) on the screen at their current position
        """
        player_positions = self.ask_server('get_all_positions')

        for character, position in player_positions.items():
            square = self.board.get_mapping(position)
            x, y = square[0], square[1]
            x_length, y_length = square[2], square[3]

            center_x = x + (x_length // 2)
            center_y = y + (y_length // 2)

            pygame.draw.circle(self.WIN, constants.BLACK, (center_x, center_y), (x_length // 2.5) + 3)
            font = pygame.font.SysFont('freesansbold.ttf', 18)

            if character == Characters.COLONEL_MUSTARD.value:
                pygame.draw.circle(self.WIN, constants.MUSTARD, (center_x, center_y), x_length // 2.5)
                self.WIN.blit(font.render('M', True, constants.BLACK), (center_x - 5, center_y - 5))
            elif character == Characters.MRS_WHITE.value:
                pygame.draw.circle(self.WIN, constants.WHITE, (center_x, center_y), x_length // 2.5)
                self.WIN.blit(font.render('W', True, constants.BLACK), (center_x - 5, center_y - 5))
            elif character == Characters.MRS_PEACOCK.value:
                pygame.draw.circle(self.WIN, constants.PEACOCK, (center_x, center_y), x_length // 2.5)
                self.WIN.blit(font.render('PK', True, constants.BLACK), (center_x - 8, center_y - 5))
            elif character == Characters.MISS_SCARLET.value:
                pygame.draw.circle(self.WIN, constants.SCARLET, (center_x, center_y), x_length // 2.5)
                self.WIN.blit(font.render('S', True, constants.BLACK), (center_x - 4, center_y - 5))
            elif character == Characters.PROFESSOR_PLUM.value:
                pygame.draw.circle(self.WIN, constants.PLUM, (center_x, center_y), x_length // 2.5)
                self.WIN.blit(font.render('PL', True, constants.BLACK), (center_x - 8, center_y - 5))
            else:
                pygame.draw.circle(self.WIN, constants.GREEN, (center_x, center_y), x_length // 2.5)
                self.WIN.blit(font.render('G', True, constants.BLACK), (center_x - 5, center_y - 5))

    def draw_turn(self, player):
        """
        Draws an indicator that tells the player whose turn it is
        :param player: Character whose turn it is
        """
        self.draw_text(f"It's {player.get_character().value}'s turn", 24, constants.BLACK, 700, 725)

    def draw_moves(self, move):
        """
        Draws an indicator that tells the player how many moves they have left
        :param move: Integer of how many moves are left
        """
        self.draw_text(f'You have {move} moves left', 24, constants.SCARLET, 700, 700)

    def draw_notes(self):
        """
        Draws information that tells the player what they already know in relation to the murder mystery
        """
        font = pygame.font.SysFont('freesansbold.ttf', 20)
        if self.character:
            self.draw_text(f"{self.character.value}'s notes", 32, constants.BLACK, 675, 20)

        all_cards = Deck.all_values()

        # Characters
        self.draw_text("Potential Murder Suspects", 24, constants.BLACK, 675, 75)
        for i, character in enumerate(all_cards[0]):
            x = 675 + (i//3 * 125)
            y = 100 + ((i % 3) * 20)
            self.WIN.blit(font.render(f"{character}", True, constants.BLACK), (x, y))

            if self.notes and character in self.notes[0]:
                pygame.draw.line(self.WIN, constants.BLACK, (x, y+6), (x + len(character)*7, y+6), 2)

        # Weapons
        self.draw_text("Potential Murder Weapons", 24, constants.BLACK, 675, 200)
        for i, weapon in enumerate(all_cards[1]):
            x = 675 + (i//3 * 125)
            y = 225 + ((i % 3) * 20)

            self.WIN.blit(font.render(f"{weapon}", True, constants.BLACK), (x, y))

            if self.notes and weapon in self.notes[1]:
                pygame.draw.line(self.WIN, constants.BLACK, (x, y + 6), (x + len(weapon)*7, y + 6), 2)

        # Locations
        self.draw_text("Potential Murder Locations", 24, constants.BLACK, 675, 325)
        for i, location in enumerate(all_cards[2]):
            x = 630 + (i//3 * 125)
            y = 350 + ((i % 3) * 20)

            self.WIN.blit(font.render(f"{location}", True, constants.BLACK), (x, y))

            if self.notes and location in self.notes[2]:
                pygame.draw.line(self.WIN, constants.BLACK, (x, y + 6), (x + len(location)*7, y + 6), 2)

    def draw_cards(self):
        """
        Draws the visual of the cards being held by the player
        """
        font = pygame.font.SysFont('freesansbold.ttf', 14)
        self.draw_text('Your cards', 20, constants.BLACK, 265, 635)

        for i, card in enumerate(self.cards):
            x = 10 + ((i % 6) * 100)
            y = 655 + (30 * (i // 6))

            # Card background
            self.draw_box(x, y, constants.CARD_SIZE_X, constants.CARD_SIZE_Y, constants.CARD)
            card_value = card.get_value()

            # Card text
            self.WIN.blit(font.render(f'{card_value}', True, constants.BLACK),
                          (x + 2.5*(17 - len(card_value)), y + 5))

    def occupied(self, space) -> bool:
        """
        Shows whether a position is occupied by a player
        :param space: ID of the space (int)
        :return: Bool
        """
        self.update_player_positions()
        for key in self.player_positions.keys():
            if space == self.player_positions[key]:
                return True

        return False

    def calculate_valid_moves(self) -> [str]:
        # TODO: Need to do more handling now that doors are one directional
        """
        Calculates which direction the player can move from their current position
        """
        directions = []
        self.update_player_positions()
        position = self.player_positions[self.character.value]

        # Check for valid movements (right, left, down, up).
        dr = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        row = position // 24
        col = position % 24
        ind = 0
        for r, c in dr:
            nr = row + r
            nc = col + c
            space_id = (nr * 24) + nc

            # Verify that the rows and columns are within the proper ranges
            if 0 <= nr < 25 and 0 <= nc < 24:
                if (not self.occupied(space_id) and self.board.board[space_id].get_room()) ==\
                        RoomType.HALLWAY or Board.is_entrance(space_id):
                    # Add the position to the valid directions dictionary
                    if ind == 0:
                        directions.append('Right')
                    elif ind == 1:
                        directions.append('Left')
                    elif ind == 2:
                        directions.append('Down')
                    else:
                        directions.append('Up')
            ind += 1

        return directions

    def populate_rooms(self):
        """
        Updates the board to reflect people being in a certain room
        :return: None
        """
        self.update_player_positions()
        self.board.refresh_room_occupied()

        for player in self.player_positions.keys():
            room = self.board.what_room(self.player_positions[player])

            if room not in ['Hallway', 'OFB', 'Start']:
                if self.player_positions[player] in self.board.room_display[room]:
                    index = self.board.room_display[room].index(self.player_positions[player])
                    self.board.room_occupied[room][index] = True

    def give_room_position(self, player_position) -> int:
        # TODO: May need to come here to do stuff server side
        """
        When the player enters a room, they will be given an available display position within the room
        :param player_position: Integer of our position
        :return: ID of new player position (int)
        """

        # Figure out which room and insert the player at the next display spot
        room = self.board.what_room(player_position)
        for i in range(6):
            if self.board.room_occupied[room][i]:
                continue
            else:
                self.board.room_occupied[room][i] = True
                return self.board.room_display[room][i]

        # Shouldn't ever get here
        print("Error: Room full")
        return -1

    def free_position(self, room, position):
        """
        When the player leaves a room, this function marks their position as unoccupied.
        :param room: String representing what room the player is leaving
        :param position: The position that they were in before leaving
        :return: Nothing
        """
        if room in self.board.room_occupied:
            if position in self.board.room_display[room]:
                index = self.board.room_display[room].index(position)
                self.board.room_occupied[room][index] = False

    def pick_exit(self, room):
        """
        When there is multiple exits in a room, this function allows the user to select the one they wish to
        leave through by clicking on the space
        :param room: String representing the room name
        """
        self.draw_text(f'Select an exit from {room} by clicking on it', 24, constants.SCARLET, 630, 700)

        while True:
            # Listen for clicks
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.MOUSEBUTTONUP:
                    x2, y2 = pygame.mouse.get_pos()

                    if room in constants.ENTRANCES:
                        for entrance in constants.ENTRANCES[room]:
                            x, y, x_length, y_length = self.board.get_mapping(entrance)

                            if x <= x2 <= x + x_length and y <= y2 <= y + y_length:
                                self.update_our_position(entrance)
                                return

            pygame.display.update()

    def draw_buttons(self, room) -> str:
        """
        Allows client to make a choice of what they want to do during their turn
        :param room: String representing the room the player is in, used for secret passageways
        :return: String representing the choice the user selected
        """
        choice = ''

        # Roll Dice button
        self.draw_box(630, 455, constants.BUTTON_SIZE_X, constants.BUTTON_SIZE_Y, constants.ROLL_DICE)
        self.draw_text('Roll Dice', 22, constants.BLACK, 647, 463)

        # Suggestion button
        self.draw_box(655 + constants.BUTTON_SIZE_X, 455, constants.BUTTON_SIZE_X, constants.BUTTON_SIZE_Y,
                      constants.SUGGESTION)
        self.draw_text('Suggestion', 22, constants.BLACK, 663 + constants.BUTTON_SIZE_X, 463)

        # Accusation
        self.draw_box(680 + 2 * constants.BUTTON_SIZE_X, 455, constants.BUTTON_SIZE_X, constants.BUTTON_SIZE_Y,
                      constants.SCARLET)
        self.draw_text('Accusation', 22, constants.BLACK, 688 + 2 * constants.BUTTON_SIZE_X, 463)

        # Passage way
        if room in ['Kitchen', 'Lounge', 'Conservatory', 'Study']:
            self.draw_box(630, 480 + constants.BUTTON_SIZE_Y, constants.BUTTON_SIZE_X, constants.BUTTON_SIZE_Y,
                          constants.PASSAGE)
            self.draw_text('Passage', 18, constants.BLACK, 655, 514)

            if room == 'Kitchen':
                self.draw_text('To Study', 18, constants.BLACK, 655, 525)
            elif room == 'Study':
                self.draw_text('To Kitchen', 18, constants.BLACK, 648, 525)
            elif room == 'Conservatory':
                self.draw_text('To Lounge', 18, constants.BLACK, 650, 525)
            elif room == 'Lounge':
                self.draw_text('To Conservatory', 18, constants.BLACK, 633, 525)

        pygame.event.clear()

        while choice == '':
            # Listen for clicks
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    x, y = pos

                    # Check if they clicked the roll dice button
                    if 630 <= x <= 630 + constants.BUTTON_SIZE_X and 455 <= y <= 455 + constants.BUTTON_SIZE_Y:
                        choice = 'Move'
                    elif 655 + constants.BUTTON_SIZE_X <= x <= 655 + 2 * constants.BUTTON_SIZE_X and \
                            455 <= y <= 455 + constants.BUTTON_SIZE_Y:
                        choice = 'Suggestion'

                    elif 680 + 2 * constants.BUTTON_SIZE_X <= x <= 680 + 3 * constants.BUTTON_SIZE_X and \
                            455 <= y <= 455 + constants.BUTTON_SIZE_Y:
                        choice = 'Accusation'

                    elif 630 <= x <= 630 + constants.BUTTON_SIZE_X and \
                            480 + constants.BUTTON_SIZE_Y <= y <= 480 + 2 * constants.BUTTON_SIZE_Y:
                        choice = 'Passage'

            pygame.display.update()

        return choice

    def suggest_or_pass(self, room):
        """
        When a player enters a room, they need to have the option to make an accusation
        :param room: String of what room the player is located in
        :return: None
        """

        # Suggestion
        self.draw_box(630, 455, constants.BUTTON_SIZE_X, constants.BUTTON_SIZE_Y, constants.SUGGESTION)
        self.draw_text('Suggestion', 22, constants.BLACK, 639, 463)

        # Pass
        self.draw_box(655 + constants.BUTTON_SIZE_X, 455, constants.BUTTON_SIZE_X, constants.BUTTON_SIZE_Y,
                      constants.SCARLET)
        self.draw_text('Pass', 22, constants.BLACK, 688 + constants.BUTTON_SIZE_X, 463)

        pygame.display.update()
        pygame.event.clear()

        choice = None
        while not choice:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    x, y = pos

                    # Check if they clicked the roll dice button
                    if 630 <= x <= 630 + constants.BUTTON_SIZE_X and 455 <= y <= 455 + constants.BUTTON_SIZE_Y:
                        choice = 'Suggestion'
                    elif 655 + constants.BUTTON_SIZE_X <= x <= 655 + 2 * constants.BUTTON_SIZE_X and \
                            455 <= y <= 455 + constants.BUTTON_SIZE_Y:
                        choice = 'Pass'

            pygame.display.flip()

        pygame.event.clear()

        if choice == 'Suggestion':
            self.make_suggestion(room)

    def accusation_or_pass(self):
        """
        When a player does not receive an answer to a suggestion, they may make an accusation
        :return: Nothing
        """
        self.WIN.fill(constants.BACKGROUND)

        # Display the last suggestion
        suggestion = self.ask_server('get_last_suggestion')
        sug_str = f'{suggestion.get_character()} with the {suggestion.get_weapon()} in the {suggestion.get_room()}'

        # Trying to center this
        if len(sug_str) <= 40:
            self.draw_text(sug_str, 40, constants.BLACK, 235, 60)
        elif len(sug_str) <= 50:
            self.draw_text(sug_str, 40, constants.BLACK, 215, 60)
        elif len(sug_str) <= 60:
            self.draw_text(sug_str, 40, constants.BLACK, 185, 60)
        else:
            self.draw_text(sug_str, 40, constants.BLACK, 120, 60)

        # Title
        self.draw_text('No one could disprove your suggestion', 40, constants.SCARLET, 225, 150)
        self.draw_text('Would you like to make an accusation?', 40, constants.BLACK, 225, 185)

        # Accusation
        self.draw_box(360, 250, constants.BUTTON_SIZE_X, constants.BUTTON_SIZE_Y, constants.SCARLET)
        self.draw_text('Accusation', 22, constants.BLACK, 369, 258)

        # Pass
        self.draw_box(395 + constants.BUTTON_SIZE_X, 250, constants.BUTTON_SIZE_X, constants.BUTTON_SIZE_Y,
                      constants.PASSAGE)
        self.draw_text('Pass', 22, constants.BLACK, 427 + constants.BUTTON_SIZE_X, 258)

        pygame.display.update()
        pygame.event.clear()

        choice = None
        while not choice:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    x, y = pos

                    # Check if they clicked the roll dice button
                    if 360 <= x <= 360 + constants.BUTTON_SIZE_X and 250 <= y <= 250 + constants.BUTTON_SIZE_Y:
                        choice = 'Accusation'
                    elif 395 + constants.BUTTON_SIZE_X <= x <= 395 + 2 * constants.BUTTON_SIZE_X and \
                            250 <= y <= 250 + constants.BUTTON_SIZE_Y:
                        choice = 'Pass'

        pygame.event.clear()

        if choice == 'Accusation':
            self.handle_accusation()

    def roll_dice(self, exiting):
        """
        Simulates a double dice roll and handles the movement
        :param exiting: Boolean of if the player is leaving a room or not
        """
        self.update_player_positions()

        # How many spaces the player can move during their turn (equivalent to rolling 2 dice)
        moves = random.randint(2, 12)
        pygame.event.clear()

        while moves > 0:
            valid_moves = self.calculate_valid_moves()
            ev = pygame.event.get()
            for event in ev:

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RIGHT:
                        if 'Right' in valid_moves:
                            self.player_positions[self.character.value] += 1
                            moves -= 1
                            exiting = False

                    elif event.key == pygame.K_LEFT:
                        if 'Left' in valid_moves:
                            self.player_positions[self.character.value] -= 1
                            moves -= 1
                            exiting = False

                    elif event.key == pygame.K_DOWN:
                        if 'Down' in valid_moves:
                            self.player_positions[self.character.value] += 24
                            moves -= 1
                            exiting = False

                    elif event.key == pygame.K_UP:
                        if 'Up' in valid_moves:
                            self.player_positions[self.character.value] -= 24
                            moves -= 1
                            exiting = False

            # Handle a player entering the room
            if not exiting and Board.is_entrance(self.player_positions[self.character.value]):
                moves = 0
                # Give them the illusion of actually entering the room
                self.update_our_position(self.player_positions[self.character.value])
                self.draw_screen()
                self.draw_moves(moves)

                self.player_positions[self.character.value] = \
                    self.give_room_position(self.player_positions[self.character.value])
                self.suggest_or_pass(self.board.what_room(self.player_positions[self.character.value]))

            self.draw_screen()
            self.draw_moves(moves)
            self.update_our_position(self.player_positions[self.character.value])
            pygame.display.update()


    def make_suggestion(self, room) -> str:
        """
        Handles selection for suggestions, tells suggestion to the server and waits for a response
        :param room: String representing room player is in
        :return: Optional string
        """
        char = None
        weapon = None

        font = pygame.font.SysFont('freesansbold.ttf', 26)

        confirm = False
        run = True
        while run:
            self. WIN.fill(constants.BACKGROUND)
            self.draw_notes()
            self.draw_text('Select a character', 30, constants.BLACK, 25, 75)
            self.draw_text('Select a weapon', 30, constants.BLACK, 25, 225)
            self.characters_group.draw(self.WIN)
            self.weapons_group.draw(self.WIN)

            # Title
            self.draw_text('Make a suggestion', 60, constants.BLACK, 125, 20)

            # Displays choices to the user
            self.WIN.blit(font.render('Character: ', True, constants.BLACK), (25, 400))
            if char:
                self.WIN.blit(font.render(f'{char}', True, constants.BLACK), (120, 400))

            self.WIN.blit(font.render('Weapon: ', True, constants.BLACK), (275, 400))
            if weapon:
                self.WIN.blit(font.render(f'{weapon}', True, constants.BLACK), (350, 400))

            self.WIN.blit(font.render(f'Room: {room}', True, constants.BLACK), (25, 450))

            # Confirm button
            self.draw_box(175, 675, constants.SUGGESTION_BUTTONS_X, constants.SUGGESTION_BUTTONS_Y, constants.GREEN)
            self.WIN.blit(font.render('Confirm', True, constants.BLACK), (207, 683))

            # Cancel button
            self.draw_box(325, 675, constants.SUGGESTION_BUTTONS_X, constants.SUGGESTION_BUTTONS_Y, constants.SCARLET)
            self.WIN.blit(font.render('Cancel', True, constants.BLACK), (357, 683))

            # Check for button clicks
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()

                    # Characters - Colonel Mustard
                    if 25 <= x <= 25 + constants.SUGGESTION_BUTTONS_X \
                            and 100 <= y <= 100 + constants.SUGGESTION_BUTTONS_Y:
                        char = 'Colonel Mustard'
                    elif 175 <= x <= 175 + constants.SUGGESTION_BUTTONS_X \
                            and 100 <= y <= 100 + constants.SUGGESTION_BUTTONS_Y:
                        char = 'Miss Scarlet'
                    elif 325 <= x <= 325 + constants.SUGGESTION_BUTTONS_X \
                            and 100 <= y <= 100 + constants.SUGGESTION_BUTTONS_Y:
                        char = 'Mrs.White'
                    elif 475 <= x <= 475 + constants.SUGGESTION_BUTTONS_X \
                            and 100 <= y <= 100 + constants.SUGGESTION_BUTTONS_Y:
                        char = 'Reverend Green'
                    elif 25 <= x <= 25 + constants.SUGGESTION_BUTTONS_X \
                            and 150 <= y <= 150 + constants.SUGGESTION_BUTTONS_Y:
                        char = 'Mrs.Peacock'
                    elif 175 <= x <= 175 + constants.SUGGESTION_BUTTONS_X \
                            and 150 <= y <= 150 + constants.SUGGESTION_BUTTONS_Y:
                        char = 'Professor Plum'
                    elif 25 <= x <= 25 + constants.SUGGESTION_BUTTONS_X \
                            and 250 <= y <= 250 + constants.SUGGESTION_BUTTONS_Y:
                        weapon = 'Knife'
                    elif 175 <= x <= 175 + constants.SUGGESTION_BUTTONS_X \
                            and 250 <= y <= 250 + constants.SUGGESTION_BUTTONS_Y:
                        weapon = 'Candle stick'
                    elif 325 <= x <= 325 + constants.SUGGESTION_BUTTONS_X \
                            and 250 <= y <= 250 + constants.SUGGESTION_BUTTONS_Y:
                        weapon = 'Revolver'
                    elif 475 <= x <= 475 + constants.SUGGESTION_BUTTONS_X \
                            and 250 <= y <= 250 + constants.SUGGESTION_BUTTONS_Y:
                        weapon = 'Rope'
                    elif 25 <= x <= 25 + constants.SUGGESTION_BUTTONS_X \
                            and 300 <= y <= 300 + constants.SUGGESTION_BUTTONS_Y:
                        weapon = 'Lead pipe'
                    elif 175 <= x <= 175 + constants.SUGGESTION_BUTTONS_X \
                            and 300 <= y <= 300 + constants.SUGGESTION_BUTTONS_Y:
                        weapon = 'Wrench'
                    elif 175 <= x <= 175 + constants.SUGGESTION_BUTTONS_X \
                            and 675 <= y <= 675 + constants.SUGGESTION_BUTTONS_Y:
                        if weapon and char:
                            confirm = True
                            run = False
                    elif 325 <= x <= 325 + constants.SUGGESTION_BUTTONS_X \
                            and 675 <= y <= 675 + constants.SUGGESTION_BUTTONS_Y:
                        run = False

            pygame.display.update()

        if confirm:
            self.ask_server(f'make_suggestion {char},{weapon},{room}')
            ready = self.ask_server('check_suggestion_status')
            title = pygame.font.SysFont('freesansbold.ttf', 40)

            while ready:
                c = self.ask_server('waiting_on')
                self.WIN.fill(constants.BACKGROUND)
                self.WIN.blit(title.render(f'{char} with the {weapon} in the {room}', True, constants.BLACK),
                              (150, 100))
                self.WIN.blit(title.render(f'Waiting on {c.get_character().value} to respond', True, constants.BLACK),
                              (240, 150))
                pygame.display.update()
                time.sleep(1)
                ready = self.ask_server('check_suggestion_status')

            # Get response
            response = self.ask_server('get_suggestion_response')

            if response != 'No one could disprove':
                self.ask_server(f'add_note {response}')
            else:
                self.accusation_or_pass()

        # Cancel button was pressed
        else:
            return 'Cancelled'

    def draw_related_cards(self, related_cards, player) -> {str: (int, int)}:
        """
        Draws cards for answering suggestions
        :param related_cards: Array of card objects
        :param player: String of players name
        :return: Dictionary mapping {card value (str) -> (x , y) positions (int, int)}
        """
        font = pygame.font.SysFont('freesansbold.ttf', 26)
        self.draw_text(f'Select a card to disprove {player}s suggestion', 36, constants.BLACK, 175, 200)
        related_map = {}

        if len(related_cards) > 0:
            for i, card in enumerate(related_cards):
                x = 175 + (i * 200)
                y = 250

                # Card background
                self.draw_box(x, y, 2 * constants.CARD_SIZE_X, 2 * constants.CARD_SIZE_Y, constants.CARD)

                # Card text
                card_value = card.get_value()
                related_map[card_value] = (x, y)
                self.WIN.blit(font.render(f'{card_value}', True, constants.BLACK),
                              (x + 4 * (20 - len(card_value)), y + 13))

        else:
            self.draw_text('You have no related cards to show', 36, constants.BLACK, 300, 400)

        return related_map

    def respond_suggestion(self):
        """
        Handles the choice of card to show during a suggestion
        :return: Nothing
        """
        suggestion = self.ask_server('get_last_suggestion')

        related_cards = []
        for card in self.cards:
            if card.get_category().value == 'CHARACTER':
                if card.get_value() == suggestion.get_character():
                    related_cards.append(card)
            elif card.get_category().value == 'WEAPON':
                if card.get_value() == suggestion.get_weapon():
                    related_cards.append(card)
            elif card.get_category().value == 'PLACE':
                if card.get_value() == suggestion.get_room():
                    related_cards.append(card)

        confirm = False
        card_choice = None
        while not confirm:
            self.WIN.fill(constants.BACKGROUND)
            # Title
            self.draw_text(f'{suggestion.get_player()} has made a suggestion', 46, constants.BLACK, 225, 20)
            suggest_text = \
                f'{suggestion.get_character()} with the {suggestion.get_weapon()} in the {suggestion.get_room()}'

            if len(suggest_text) <= 40:
                self.draw_text(suggest_text, 30, constants.SCARLET, 260, 150)
            elif len(suggest_text) <= 50:
                self.draw_text(suggest_text, 30, constants.SCARLET, 230, 150)
            else:
                self.draw_text(suggest_text, 30, constants.SCARLET, 200, 150)

            # Cards
            related_map = self.draw_related_cards(related_cards, suggestion.get_player())

            # Confirmation background
            self.draw_text(f'You have selected: {card_choice}', 28, constants.BLACK, 375, 600)
            self.draw_box(400, 650, 2 * constants.BUTTON_SIZE_X, 2 * constants.BUTTON_SIZE_Y, constants.GREEN)
            self.draw_text('Confirm', 28, constants.BLACK, 460, 672)

            # Listen for clicks
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()

                    # Find out if the click maps to a character
                    for key in related_map.keys():
                        x, y = pos
                        x2, y2 = related_map[key]

                        if x2 < x < x2 + (2 * constants.CARD_SIZE_X) and \
                                y2 < y < y2 + (2 * constants.CARD_SIZE_Y):
                            card_choice = key

                    # Clicking confirmed
                    x, y = pos
                    if 400 <= x <= 400 + 2*constants.BUTTON_SIZE_X and 650 <= y <= 650 + 2*constants.BUTTON_SIZE_Y:
                        if len(related_cards) == 0 or card_choice:
                            confirm = True

            pygame.display.update()

        if card_choice:
            self.ask_server(f'answer_suggestion {card_choice}')
        else:
            self.ask_server('next_player')

    def handle_accusation(self) -> str:
        """
        Handles selections for accusation, sends it into the server
        :return: Optional String
        """
        char = None
        weapon = None
        room = None

        confirm = False
        flag = False

        font = pygame.font.SysFont('freesansbold.ttf', 24)

        while not flag:
            # Set the screen
            self.WIN.fill(constants.BACKGROUND)
            self.draw_notes()
            self.draw_text('Select a character', 30, constants.BLACK, 25, 75)
            self.draw_text('Select a weapon', 30, constants.BLACK, 25, 225)
            self.draw_text('Select a room', 30, constants.BLACK, 25, 375)
            self.characters_group.draw(self.WIN)
            self.weapons_group.draw(self.WIN)
            self.rooms_group.draw(self.WIN)

            # Section title
            self.draw_text('Make an Accusation', 60, constants.BLACK, 125, 20)

            # Displays choices to the user
            self.WIN.blit(font.render('Character: ', True, constants.BLACK), (25, 550))
            if char:
                self.WIN.blit(font.render(f'{char}', True, constants.BLACK), (120, 550))

            self.WIN.blit(font.render('Weapon: ', True, constants.BLACK), (275, 550))
            if weapon:
                self.WIN.blit(font.render(f'{weapon}', True, constants.BLACK), (350, 550))

            self.WIN.blit(font.render(f'Room: ', True, constants.BLACK), (480, 550))
            if room:
                self.WIN.blit(font.render(f'{room}', True, constants.BLACK), (540, 550))

            # Confirm button
            self.draw_box(175, 675, constants.SUGGESTION_BUTTONS_X, constants.SUGGESTION_BUTTONS_Y, constants.GREEN)
            self.WIN.blit(font.render('Confirm', True, constants.BLACK), (207, 683))

            # Cancel button
            self.draw_box(325, 675, constants.SUGGESTION_BUTTONS_X, constants.SUGGESTION_BUTTONS_Y, constants.SCARLET)
            self.WIN.blit(font.render('Cancel', True, constants.BLACK), (357, 683))

            # Disclaimer
            self.draw_text('WARNING', 36, constants.SCARLET, 725, 625)
            self.draw_text('An incorrect accusation leads to disqualification', 20, constants.BLACK, 625, 660)
            self.draw_text('You will lose your turns, and may only respond to suggestions', 20, constants.BLACK, 590,
                           690)

            # Check for button clicks
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()

                    # Characters - Colonel Mustard
                    if 25 <= x <= 25 + constants.SUGGESTION_BUTTONS_X \
                            and 100 <= y <= 100 + constants.SUGGESTION_BUTTONS_Y:
                        char = 'Colonel Mustard'
                    elif 175 <= x <= 175 + constants.SUGGESTION_BUTTONS_X \
                            and 100 <= y <= 100 + constants.SUGGESTION_BUTTONS_Y:
                        char = 'Miss Scarlet'
                    elif 325 <= x <= 325 + constants.SUGGESTION_BUTTONS_X \
                            and 100 <= y <= 100 + constants.SUGGESTION_BUTTONS_Y:
                        char = 'Mrs.White'
                    elif 475 <= x <= 475 + constants.SUGGESTION_BUTTONS_X \
                            and 100 <= y <= 100 + constants.SUGGESTION_BUTTONS_Y:
                        char = 'Reverend Green'
                    elif 25 <= x <= 25 + constants.SUGGESTION_BUTTONS_X \
                            and 150 <= y <= 150 + constants.SUGGESTION_BUTTONS_Y:
                        char = 'Mrs.Peacock'
                    elif 175 <= x <= 175 + constants.SUGGESTION_BUTTONS_X \
                            and 150 <= y <= 150 + constants.SUGGESTION_BUTTONS_Y:
                        char = 'Professor Plum'
                    elif 25 <= x <= 25 + constants.SUGGESTION_BUTTONS_X \
                            and 250 <= y <= 250 + constants.SUGGESTION_BUTTONS_Y:
                        weapon = 'Knife'
                    elif 175 <= x <= 175 + constants.SUGGESTION_BUTTONS_X \
                            and 250 <= y <= 250 + constants.SUGGESTION_BUTTONS_Y:
                        weapon = 'Candle stick'
                    elif 325 <= x <= 325 + constants.SUGGESTION_BUTTONS_X \
                            and 250 <= y <= 250 + constants.SUGGESTION_BUTTONS_Y:
                        weapon = 'Revolver'
                    elif 475 <= x <= 475 + constants.SUGGESTION_BUTTONS_X \
                            and 250 <= y <= 250 + constants.SUGGESTION_BUTTONS_Y:
                        weapon = 'Rope'
                    elif 25 <= x <= 25 + constants.SUGGESTION_BUTTONS_X \
                            and 300 <= y <= 300 + constants.SUGGESTION_BUTTONS_Y:
                        weapon = 'Lead pipe'
                    elif 175 <= x <= 175 + constants.SUGGESTION_BUTTONS_X \
                            and 300 <= y <= 300 + constants.SUGGESTION_BUTTONS_Y:
                        weapon = 'Wrench'
                    elif 25 <= x <= 25 + constants.SUGGESTION_BUTTONS_X \
                            and 400 <= y <= 400 + constants.SUGGESTION_BUTTONS_Y:
                        room = 'Hall'
                    elif 175 <= x <= 175 + constants.SUGGESTION_BUTTONS_X \
                            and 400 <= y <= 400 + constants.SUGGESTION_BUTTONS_Y:
                        room = 'Lounge'
                    elif 325 <= x <= 325 + constants.SUGGESTION_BUTTONS_X \
                            and 400 <= y <= 400 + constants.SUGGESTION_BUTTONS_Y:
                        room = 'Dining Room'
                    elif 475 <= x <= 475 + constants.SUGGESTION_BUTTONS_X \
                            and 400 <= y <= 400 + constants.SUGGESTION_BUTTONS_Y:
                        room = 'Kitchen'
                    elif 25 <= x <= 25 + constants.SUGGESTION_BUTTONS_X \
                            and 450 <= y <= 450 + constants.SUGGESTION_BUTTONS_Y:
                        room = 'Ballroom'
                    elif 175 <= x <= 175 + constants.SUGGESTION_BUTTONS_X \
                            and 450 <= y <= 450 + constants.SUGGESTION_BUTTONS_Y:
                        room = 'Conservatory'
                    elif 325 <= x <= 325 + constants.SUGGESTION_BUTTONS_X \
                            and 450 <= y <= 450 + constants.SUGGESTION_BUTTONS_Y:
                        room = 'Billiard Room'
                    elif 475 <= x <= 475 + constants.SUGGESTION_BUTTONS_X \
                            and 450 <= y <= 450 + constants.SUGGESTION_BUTTONS_Y:
                        room = 'Library'
                    elif 25 <= x <= 25 + constants.SUGGESTION_BUTTONS_X \
                            and 500 <= y <= 500 + constants.SUGGESTION_BUTTONS_Y:
                        room = 'Study'

                    # Confirm button
                    elif 175 <= x <= 175 + constants.SUGGESTION_BUTTONS_X \
                            and 675 <= y <= 675 + constants.SUGGESTION_BUTTONS_Y:
                        if char and weapon and room:
                            confirm = True
                            flag = True

                    # Cancel button
                    elif 325 <= x <= 325 + constants.SUGGESTION_BUTTONS_X \
                            and 675 <= y <= 675 + constants.SUGGESTION_BUTTONS_Y:
                        flag = True

            pygame.display.update()

        if flag and confirm:
            # Send the accusation to the server
            self.ask_server(f'make_accusation {char},{weapon},{room}')
        else:
            # Cancel button was pressed
            return 'Cancelled'

    def roll_or_accuse(self):
        # Roll Dice button
        self.draw_box(630, 455, constants.BUTTON_SIZE_X, constants.BUTTON_SIZE_Y, constants.ROLL_DICE)
        self.draw_text('Roll Dice', 22, constants.BLACK, 647, 463)

        # Accusation button
        self.draw_box(655 + constants.BUTTON_SIZE_X, 455, constants.BUTTON_SIZE_X, constants.BUTTON_SIZE_Y,
                      constants.SCARLET)
        self.draw_text('Accusation', 22, constants.BLACK, 663 + constants.BUTTON_SIZE_X, 463)

        pygame.event.clear()
        choice = ''

        while choice == '':
            # Listen for clicks
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    x, y = pos

                    # Check if they clicked the roll dice button
                    if 630 <= x <= 630 + constants.BUTTON_SIZE_X and 455 <= y <= 455 + constants.BUTTON_SIZE_Y:
                        choice = 'Move'
                    elif 655 + constants.BUTTON_SIZE_X <= x <= 655 + 2 * constants.BUTTON_SIZE_X and \
                            455 <= y <= 455 + constants.BUTTON_SIZE_Y:
                        choice = 'Accusation'

            pygame.display.update()

        return choice

    def handle_turn(self):
        """
        Primary function in charge of managing players turn
        :return: Nothing
        """
        self.draw_screen()
        pygame.display.update()

        player_positions = self.ask_server('get_all_positions')

        self.populate_rooms()
        room = self.board.what_room(player_positions[self.character.value])

        # If they are in a room
        if room not in ['Hallway', 'OFB', 'Start']:
            # Allow them to choose to move, make a suggestion, use a passageway, or make an accusation
            choice = self.draw_buttons(room)

            if choice == 'Move':
                # Free the position in the room
                self.free_position(room, player_positions[self.character.value])

                # If there's multiple exits, let the player choose which one they want to leave from
                if len(constants.ENTRANCES[room]) > 1:
                    self.pick_exit(room)
                    self.update_player_positions()
                else:
                    self.update_our_position(constants.ENTRANCES[room][0])
                    self.update_player_positions()

                self.roll_dice(True)

            elif choice == 'Suggestion':
                status = self.make_suggestion(room)
                if status == 'Cancelled':
                    return self.handle_turn()

            elif choice == 'Accusation':
                status = self.handle_accusation()
                if status and status == 'Cancelled':
                    return self.handle_turn()

            elif choice == 'Passage':
                if room == 'Kitchen':
                    self.player_positions[self.character.value] = constants.ENTRANCES['Study'][0]
                elif room == 'Study':
                    self.player_positions[self.character.value] = constants.ENTRANCES['Kitchen'][0]
                elif room == 'Conservatory':
                    self.player_positions[self.character.value] = constants.ENTRANCES['Lounge'][0]
                elif room == 'Lounge':
                    self.player_positions[self.character.value] = constants.ENTRANCES['Conservatory'][0]

                self.player_positions[self.character.value] = \
                    self.give_room_position(player_positions[self.character.value])
                self.update_our_position(self.player_positions[self.character.value])

                self.draw_screen()
                room = self.board.what_room(player_positions[self.character.value])
                pygame.display.update()

                self.suggest_or_pass(room)

        else:
            # Roll the Dice, or make an accusation
            choice = self.roll_or_accuse()
            if choice == 'Move':
                self.roll_dice(False)
            elif choice == 'Accusation':
                status = self.handle_accusation()
                if status and status == 'Cancelled':
                    return self.handle_turn()

        # Tell the server the turn is done
        self.ask_server('turn_done')

# This section handles the end of the game visuals
    def draw_disqualification(self):
        """
        Draws the disqualification message
        """
        self.draw_text('You have been disqualified', 20, constants.SCARLET, 700, 430)
        self.draw_text('You have lost your turn, but still must answer suggestions', 20, constants.BLACK, 610, 450)

    def draw_end_screen(self):
        """
        Draws end game screen that displays the winner
        :return: Nothing
        """
        winner = self.ask_server('get_winner')
        envelope = self.ask_server('get_envelope')
        run = True

        while run:
            self.WIN.fill(constants.BACKGROUND)

            # Winner title
            if winner == self.character.value:
                self.draw_text('Congratulations! You Won!', 60, constants.BLACK, 225, 100)
            elif not winner:
                self.draw_text('Everyone Disqualified! You Lose!', 60, constants.BLACK, 175, 100)
            else:
                self.draw_text(f'{winner} Won!', 60, constants.BLACK, 275 + 5 * (18 - len(winner)), 100)

            # Display envelope
            self.draw_text(envelope.get_character(), 56, constants.SCARLET, 100, 225)
            self.draw_text('with the', 46, constants.BLACK, 300, 335)
            self.draw_text(envelope.get_weapon(), 56, constants.SCARLET, 440, 335)
            self.draw_text('in the', 46, constants.BLACK, 600, 445)
            self.draw_text(envelope.get_room(), 56, constants.SCARLET, 700, 445)

            # Quit button
            self.draw_box(300, 600, 3 * constants.SUGGESTION_BUTTONS_X, 3 * constants.SUGGESTION_BUTTONS_Y,
                          constants.GREEN)
            self.draw_text('Quit', 60, constants.BLACK, 435, 625)

            for event in pygame.event.get():
                # Force quit
                if event.type == pygame.QUIT:
                    run = False

                # Quit button
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()

                    if 300 <= x <= 300 + 3*constants.SUGGESTION_BUTTONS_X \
                            and 600 <= y <= 600 + 3*constants.SUGGESTION_BUTTONS_Y:
                        run = False

            pygame.display.update()
