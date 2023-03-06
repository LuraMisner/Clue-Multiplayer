import constants
import pygame
import random
import time
from board import Board
from characters import Characters
from deck import Deck
from network import Network
from roomtype import RoomType


WIN = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Clue")
pygame.init()

n = Network()
log = []


def draw_screen(board, cards, character, notes, player_positions, current_turn):
    """
    Used to call all the individual functions that make up the components of the GUI
    :param board: Board object to reflect the board being shown
    :param cards: Array of Card objects to represent the players cards
    :param character: Character object reflecting our player
    :param notes: Array of information gathered throughout the game Index 0: Characters, 1: Weapons, 2: Locations
    :param player_positions: Dictionary mapping {characters name (str) -> position on board (int)}
    :param current_turn: String representing the name of the character whose turn it is
    :return: Nothing
    """
    board.draw_board()
    draw_players(player_positions, board)
    draw_cards(cards)
    draw_notes(character.value, notes)
    draw_turn(current_turn)


def draw_players(player_positions, board):
    """
    Draws the player piece (circle) on the screen at their current position
    :param player_positions: Dictionary mapping {characters name (str) -> position on board (int)}
    :param board:  Board object that represents the board
    :return: Nothing
    """
    for character, position in player_positions.items():
        square = board.get_mapping(position)
        x, y = square[0], square[1]
        x_length, y_length = square[2], square[3]

        center_x = x + (x_length // 2)
        center_y = y + (y_length // 2)

        pygame.draw.circle(WIN, constants.BLACK, (center_x, center_y), (x_length // 2.5) + 3)
        font = pygame.font.SysFont('freesansbold.ttf', 18)

        if character == Characters.COLONEL_MUSTARD.value:
            pygame.draw.circle(WIN, constants.MUSTARD, (center_x, center_y), x_length // 2.5)
            WIN.blit(font.render('M', True, constants.BLACK), (center_x - 5, center_y - 5))
        elif character == Characters.MRS_WHITE.value:
            pygame.draw.circle(WIN, constants.WHITE, (center_x, center_y), x_length // 2.5)
            WIN.blit(font.render('W', True, constants.BLACK), (center_x - 5, center_y - 5))
        elif character == Characters.MR_PEACOCK.value:
            pygame.draw.circle(WIN, constants.PEACOCK, (center_x, center_y), x_length // 2.5)
            WIN.blit(font.render('PK', True, constants.BLACK), (center_x - 8, center_y - 5))
        elif character == Characters.MISS_SCARLET.value:
            pygame.draw.circle(WIN, constants.SCARLET, (center_x, center_y), x_length // 2.5)
            WIN.blit(font.render('S', True, constants.BLACK), (center_x - 4, center_y - 5))
        elif character == Characters.PROFESSOR_PLUM.value:
            pygame.draw.circle(WIN, constants.PLUM, (center_x, center_y), x_length // 2.5)
            WIN.blit(font.render('PL', True, constants.BLACK), (center_x - 8, center_y - 5))
        else:
            pygame.draw.circle(WIN, constants.GREEN, (center_x, center_y), x_length // 2.5)
            WIN.blit(font.render('G', True, constants.BLACK), (center_x - 5, center_y - 5))


def draw_turn(player):
    """
    Draws an indicator that tells the player whose turn it is
    :param player: Character whose turn it is
    :return: Nothing
    """
    font = pygame.font.SysFont('freesansbold.ttf', 24)
    WIN.blit(font.render(f"It's {player.get_character().value}'s turn", True, constants.BLACK), (700, 725))


def draw_moves(move):
    """
    Draws an indicator that tells the player how many moves they have left
    :param move: Integer of how many moves are left
    :return: Nothing
    """
    font = pygame.font.SysFont('freesansbold.ttf', 24)
    WIN.blit(font.render(f'You have {move} moves left', True, constants.SCARLET), (700, 700))


def draw_notes(name, notes):
    """
    Draws information that tells the player what they already know in relation to the murder mystery
    :param name: Characters name (str)
    :param notes: Information this player knows (arr length 3) Index 0: characters, Index 1: weapons, Index 2: locations
    :return: Nothing
    """
    # TODO: Redo section so that all cards you know are in black, and the ones you dont in red
    header = pygame.font.SysFont('freesansbold.ttf', 32)
    title = pygame.font.SysFont('freesansbold.ttf', 24)
    font = pygame.font.SysFont('freesansbold.ttf', 20)

    WIN.blit(header.render(f"{name}'s notes", True, constants.BLACK), (675, 30))
    all_cards = Deck.all_values()

    # Characters
    WIN.blit(title.render("Potential Murder Suspects", True, constants.BLACK), (675, 75))
    for i, character in enumerate(all_cards[0]):
        x = 675 + (i//3 * 125)
        y = 100 + ((i % 3) * 20)
        WIN.blit(font.render(f"{character}", True, constants.BLACK), (x, y))

        if character in notes[0]:
            pygame.draw.line(WIN, constants.BLACK, (x, y+6), (x + len(character)*7, y+6), 2)

    # Weapons
    WIN.blit(title.render("Potential Murder Weapons", True, constants.BLACK), (675, 200))
    for i, weapon in enumerate(all_cards[1]):
        x = 675 + (i//3 * 125)
        y = 225 + ((i % 3) * 20)

        WIN.blit(font.render(f"{weapon}", True, constants.BLACK), (x, y))

        if weapon in notes[1]:
            pygame.draw.line(WIN, constants.BLACK, (x, y + 6), (x + len(weapon)*7, y + 6), 2)

    # Locations
    WIN.blit(title.render("Potential Murder Locations", True, constants.BLACK), (675, 325))
    for i, location in enumerate(all_cards[2]):
        x = 630 + (i//3 * 125)
        y = 350 + ((i % 3) * 20)

        WIN.blit(font.render(f"{location}", True, constants.BLACK), (x, y))

        if location in notes[2]:
            pygame.draw.line(WIN, constants.BLACK, (x, y + 6), (x + len(location)*7, y + 6), 2)


def draw_cards(cards):
    """
    Draws the visual of the cards being held by the player
    :param cards: an array of Card objects that belong to the player
    :return: Nothing
    """
    title = pygame.font.SysFont('freesansbold.ttf', 20)
    font = pygame.font.SysFont('freesansbold.ttf', 14)
    WIN.blit(title.render('Your cards ', True, constants.BLACK), (265, 635))

    for i, card in enumerate(cards):
        x = 10 + ((i % 6) * 100)
        y = 655 + (30 * (i // 6))

        # Card background
        rect = pygame.Rect(x, y, constants.CARD_SIZE_X, constants.CARD_SIZE_Y)
        pygame.draw.rect(WIN, constants.CARD, rect)
        card_value = card.get_value()

        # Card text
        WIN.blit(font.render(f'{card_value}', True, constants.BLACK),
                 (x + 2.5*(17 - len(card_value)), y + 5))


def show_ready():
    """
    Creates a waiting screen for players in the game that have finished selecting their character
    :return: Nothing
    """
    # Show how many players are ready
    WIN.fill(constants.BACKGROUND)
    num_ready = n.send('num_ready')
    font = pygame.font.SysFont('freesansbold.ttf', 56)
    WIN.blit(font.render(f'Waiting on other players...', True, (0, 0, 0)), (275, 200))
    WIN.blit(font.render(f'{num_ready[1]} out of {num_ready[0]} players ready', True, constants.BLACK), (275, 275))


def select_character() -> Characters:
    """
    Draws the character selection screen and allows the player to select what character they want to be
    :return: Character object representing the character the player has chosen
    """
    selection_made = False
    choice = None

    while not selection_made:
        available_characters = n.send('character_selection')
        WIN.fill(constants.BACKGROUND)

        # How many players ready
        num_ready = n.send('num_ready')
        font1 = pygame.font.SysFont('freesansbold.ttf', 26)
        WIN.blit(font1.render(f'{num_ready[1]} out of {num_ready[0]} players ready', True, constants.BLACK), (50, 50))

        # Title
        header = pygame.font.SysFont('freesansbold.ttf', 60)
        font = pygame.font.SysFont('freesansbold.ttf', 32)
        font2 = pygame.font.SysFont('freesansbold.ttf', 26)

        WIN.blit(header.render('Select a Character', True, constants.BLACK), (300, 200))

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
            elif ch == Characters.MR_PEACOCK:
                color = constants.PEACOCK
                text1 = 'Mr.'
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

            rect = pygame.Rect(x, y, constants.CHARACTER_SELECTION_SIZE, constants.CHARACTER_SELECTION_SIZE)
            pygame.draw.rect(WIN, color, rect)
            WIN.blit(font2.render(f'{text1}', True, constants.BLACK), (x + 25 - (1.5 * len(text1)), 330))
            WIN.blit(font2.render(f'{text2}', True, constants.BLACK), (x + 25 - (1.5 * len(text2)), 355))

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
        WIN.blit(font.render('Character Selected: ', True, constants.BLACK), (300, 500))

        if choice:
            # If a choice has been made, add a confirmation button to create the player
            WIN.blit(font.render(choice.value, True, constants.BLACK), (550, 500))

            # Button to confirm selection (will confirm the selection made if choice != None
            rect = pygame.Rect(425, 600, 125, 65)
            pygame.draw.rect(WIN, (0, 0, 0), rect)
            rect = pygame.Rect(427, 602, 121, 61)
            pygame.draw.rect(WIN, (0, 255, 0), rect)

            WIN.blit(font.render('Confirm', True, constants.BLACK), (442, 622))

        pygame.display.update()

    return choice


def occupied(space, player_positions) -> bool:
    """
    Shows whether a position is occupied by a player
    :param space: ID of the space (int)
    :param player_positions: Dictionary mapping {characters name (str) -> position on board (int)}
    :return: Bool
    """
    for key in player_positions.keys():
        if space == player_positions[key]:
            return True

    return False


def calculate_valid_moves(board, character, player_positions) -> [str]:
    """
    Calculates which direction the player can move from their current position
    :param board: Board object
    :param character: Character object representing our player's character
    :param player_positions: Dictionary mapping {characters name (str) -> position on board (int)}
    :return: Nothing
    """
    directions = []
    position = player_positions[character.value]

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
            if (not occupied(space_id, player_positions) and board.board[space_id].get_room()) == RoomType.HALLWAY \
               or Board.is_entrance(space_id):
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


def populate_rooms(board, player_positions):
    """
    Updates the board to reflect people being in a certain room
    :param board: Board object
    :param player_positions: Dictionary mapping {characters name (str) -> position on board (int)}
    :return: None
    """
    board.refresh_room_occupied()

    for player in player_positions.keys():
        room = board.what_room(player_positions[player])

        if room not in ['Hallway', 'OFB', 'Start']:
            if player_positions[player] in board.room_display[room]:
                index = board.room_display[room].index(player_positions[player])
                board.room_occupied[room][index] = True


def give_room_position(board, player_position) -> int:
    """
    When the player enters a room, they will be given an available display position within the room
    :param board: Board object
    :param player_position: Dictionary mapping {characters name (str) -> position on board (int)}
    :return: ID of new player position (int)
    """

    # Figure out which room and insert the player at the next display spot
    room = board.what_room(player_position)
    for i in range(6):
        if board.room_occupied[room][i]:
            continue
        else:
            board.room_occupied[room][i] = True
            return board.room_display[room][i]

    # Shouldn't ever get here
    print("Error: Room full")
    return -1


def free_position(board, room, position):
    """
    When the player leaves a room, this function marks their position as unoccupied.
    :param board: Board object
    :param room: String representing what room the player is leaving
    :param position: The position that they were in before leaving
    :return: Nothing
    """
    if room in board.room_occupied:
        if position in board.room_display[room]:
            index = board.room_display[room].index(position)
            board.room_occupied[room][index] = False


def pick_exit(board, room) -> int:
    """
    When there is multiple exits in a room, this function allows the user to select the one they wish to leave through
    by clicking on the space
    :param board: Board object
    :param room: String representing the room name
    :return: Integer of selected entrance/exit position
    """
    font = pygame.font.SysFont('freesansbold.ttf', 24)
    WIN.blit(font.render(f'Select an exit from {room} by clicking on it', True, constants.SCARLET), (650, 700))

    while True:
        # Listen for clicks
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                x2, y2 = pygame.mouse.get_pos()

                if room in constants.ENTRANCES:
                    for entrance in constants.ENTRANCES[room]:
                        x, y, x_length, y_length = board.get_mapping(entrance)

                        if x <= x2 <= x + x_length and y <= y2 <= y + y_length:
                            return entrance
        pygame.display.update()


def draw_buttons(room) -> str:
    choice = ''
    font = pygame.font.SysFont('freesansbold.ttf', 22)
    font2 = pygame.font.SysFont('freesansbold.ttf', 18)

    # Roll Dice button
    background = pygame.Rect(630, 455, constants.BUTTON_SIZE_X, constants.BUTTON_SIZE_Y)
    pygame.draw.rect(WIN, constants.BLACK, background)
    rect = pygame.Rect(632, 457, constants.BUTTON_SIZE_X - 4, constants.BUTTON_SIZE_Y - 4)
    pygame.draw.rect(WIN, constants.ROLL_DICE, rect)
    WIN.blit(font.render('Roll Dice', True, constants.BLACK), (647, 463))

    # Suggestion button
    background = pygame.Rect(655 + constants.BUTTON_SIZE_X, 455, constants.BUTTON_SIZE_X, constants.BUTTON_SIZE_Y)
    pygame.draw.rect(WIN, constants.BLACK, background)
    rect = pygame.Rect(657 + constants.BUTTON_SIZE_X, 457, constants.BUTTON_SIZE_X - 4, constants.BUTTON_SIZE_Y - 4)
    pygame.draw.rect(WIN, constants.SUGGESTION, rect)
    WIN.blit(font.render('Suggestion', True, constants.BLACK), (663 + constants.BUTTON_SIZE_X, 463))

    # Accusation
    background = pygame.Rect(680 + 2 * constants.BUTTON_SIZE_X, 455, constants.BUTTON_SIZE_X, constants.BUTTON_SIZE_Y)
    pygame.draw.rect(WIN, constants.BLACK, background)
    rect = pygame.Rect(682 + 2 * constants.BUTTON_SIZE_X, 457, constants.BUTTON_SIZE_X - 4, constants.BUTTON_SIZE_Y - 4)
    pygame.draw.rect(WIN, constants.SCARLET, rect)
    WIN.blit(font.render('Accusation', True, constants.BLACK), (688 + 2 * constants.BUTTON_SIZE_X, 463))

    # Passage way
    if room in ['Kitchen', 'Lounge', 'Conservatory', 'Study']:
        background = pygame.Rect(630, 480 + constants.BUTTON_SIZE_Y, constants.BUTTON_SIZE_X, constants.BUTTON_SIZE_Y)
        pygame.draw.rect(WIN, constants.BLACK, background)
        rect = pygame.Rect(632, 482 + constants.BUTTON_SIZE_Y, constants.BUTTON_SIZE_X - 4, constants.BUTTON_SIZE_Y - 4)
        pygame.draw.rect(WIN, constants.PASSAGE, rect)
        WIN.blit(font2.render('Passage', True, constants.BLACK), (655, 514))

        if room == 'Kitchen':
            WIN.blit(font2.render('To Study', True, constants.BLACK), (655, 525))
        elif room == 'Study':
            WIN.blit(font2.render('To Kitchen', True, constants.BLACK), (648, 525))
        elif room == 'Conservatory':
            WIN.blit(font2.render('To Lounge', True, constants.BLACK), (650, 525))
        elif room == 'Lounge':
            WIN.blit(font2.render('To Conservatory', True, constants.BLACK), (633, 525))

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


def roll_dice(board, cards, character, notes, player_positions, current_turn, exiting) -> {str: int}:
    # How many spaces the player can move during their turn (equivalent to rolling 2 dice)
    moves = random.randint(2, 12)
    pygame.event.clear()

    while moves > 0:
        valid_moves = calculate_valid_moves(board, character, player_positions)
        ev = pygame.event.get()
        for event in ev:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT:
                    if 'Right' in valid_moves:
                        player_positions[character.value] += 1
                        moves -= 1
                        exiting = False

                elif event.key == pygame.K_LEFT:
                    if 'Left' in valid_moves:
                        player_positions[character.value] -= 1
                        moves -= 1
                        exiting = False

                elif event.key == pygame.K_DOWN:
                    if 'Down' in valid_moves:
                        player_positions[character.value] += 24
                        moves -= 1
                        exiting = False

                elif event.key == pygame.K_UP:
                    if 'Up' in valid_moves:
                        player_positions[character.value] -= 24
                        moves -= 1
                        exiting = False

        # Handle a player entering the room
        if not exiting and Board.is_entrance(player_positions[character.value]):
            # Sleep for a second to give the illusion of actually entering the room
            moves = 0
            player_positions[character.value] = give_room_position(board, player_positions[character.value])
            # TODO: Allow them to also make a suggestion

        draw_screen(board, cards, character, notes, player_positions, current_turn)
        draw_moves(moves)
        pygame.display.update()

    return player_positions


def draw_suggestion(character, notes):
    draw_notes(character.value, notes)
    title = pygame.font.SysFont('freesansbold.ttf', 30)
    font = pygame.font.SysFont('freesansbold.ttf', 20)

    WIN.blit(title.render('Select a character', True, constants.BLACK), (25, 75))
    # Characters - Colonel Mustard
    background = pygame.Rect(25, 100, constants.CHARACTER_X, constants.CHARACTER_Y)
    pygame.draw.rect(WIN, constants.BLACK, background)
    rect = pygame.Rect(27, 102, constants.CHARACTER_X - 4, constants.CHARACTER_Y - 4)
    pygame.draw.rect(WIN, constants.MUSTARD, rect)
    WIN.blit(font.render('Colonel Mustard', True, constants.BLACK), (36, 110))

    # Miss Scarlet
    background = pygame.Rect(175, 100, constants.CHARACTER_X, constants.CHARACTER_Y)
    pygame.draw.rect(WIN, constants.BLACK, background)
    rect = pygame.Rect(177, 102, constants.CHARACTER_X - 4, constants.CHARACTER_Y - 4)
    pygame.draw.rect(WIN, constants.SCARLET, rect)
    WIN.blit(font.render('Miss Scarlet', True, constants.BLACK), (198, 110))

    # Mrs. White
    background = pygame.Rect(325, 100, constants.CHARACTER_X, constants.CHARACTER_Y)
    pygame.draw.rect(WIN, constants.BLACK, background)
    rect = pygame.Rect(327, 102, constants.CHARACTER_X - 4, constants.CHARACTER_Y - 4)
    pygame.draw.rect(WIN, constants.WHITE, rect)
    WIN.blit(font.render('Mrs. White', True, constants.BLACK), (353, 110))

    # Reverend Green
    background = pygame.Rect(475, 100, constants.CHARACTER_X, constants.CHARACTER_Y)
    pygame.draw.rect(WIN, constants.BLACK, background)
    rect = pygame.Rect(477, 102, constants.CHARACTER_X - 4, constants.CHARACTER_Y - 4)
    pygame.draw.rect(WIN, constants.GREEN, rect)
    WIN.blit(font.render('Reverend Green', True, constants.BLACK), (485, 110))

    # Mr. Peacock
    background = pygame.Rect(25, 150, constants.CHARACTER_X, constants.CHARACTER_Y)
    pygame.draw.rect(WIN, constants.BLACK, background)
    rect = pygame.Rect(27, 152, constants.CHARACTER_X - 4, constants.CHARACTER_Y - 4)
    pygame.draw.rect(WIN, constants.PEACOCK, rect)
    WIN.blit(font.render('Mr. Peacock', True, constants.BLACK), (50, 160))

    # Professor Plum
    background = pygame.Rect(175, 150, constants.CHARACTER_X, constants.CHARACTER_Y)
    pygame.draw.rect(WIN, constants.BLACK, background)
    rect = pygame.Rect(177, 152, constants.CHARACTER_X - 4, constants.CHARACTER_Y - 4)
    pygame.draw.rect(WIN, constants.PLUM, rect)
    WIN.blit(font.render('Professor Plum', True, constants.BLACK), (188, 160))

    WIN.blit(title.render('Select a weapon', True, constants.BLACK), (25, 225))
    # Weapons - Knife
    background = pygame.Rect(25, 250, constants.WEAPON_X, constants.WEAPON_Y)
    pygame.draw.rect(WIN, constants.BLACK, background)
    rect = pygame.Rect(27, 252, constants.WEAPON_X - 4, constants.WEAPON_Y - 4)
    pygame.draw.rect(WIN, constants.WEAPONS, rect)
    WIN.blit(font.render('Knife', True, constants.BLACK), (70, 260))

    # Candle stick
    background = pygame.Rect(175, 250, constants.WEAPON_X, constants.WEAPON_Y)
    pygame.draw.rect(WIN, constants.BLACK, background)
    rect = pygame.Rect(177, 252, constants.WEAPON_X - 4, constants.WEAPON_Y - 4)
    pygame.draw.rect(WIN, constants.WEAPONS, rect)
    WIN.blit(font.render('Candle stick', True, constants.BLACK), (196, 260))

    # Revolver
    background = pygame.Rect(325, 250, constants.WEAPON_X, constants.WEAPON_Y)
    pygame.draw.rect(WIN, constants.BLACK, background)
    rect = pygame.Rect(327, 252, constants.WEAPON_X - 4, constants.WEAPON_Y - 4)
    pygame.draw.rect(WIN, constants.WEAPONS, rect)
    WIN.blit(font.render('Revolver', True, constants.BLACK), (357, 260))

    # Rope
    background = pygame.Rect(475, 250, constants.WEAPON_X, constants.WEAPON_Y)
    pygame.draw.rect(WIN, constants.BLACK, background)
    rect = pygame.Rect(477, 252, constants.WEAPON_X - 4, constants.WEAPON_Y - 4)
    pygame.draw.rect(WIN, constants.WEAPONS, rect)
    WIN.blit(font.render('Rope', True, constants.BLACK), (517, 260))

    # Lead Pipe
    background = pygame.Rect(25, 300, constants.WEAPON_X, constants.WEAPON_Y)
    pygame.draw.rect(WIN, constants.BLACK, background)
    rect = pygame.Rect(27, 302, constants.WEAPON_X - 4, constants.WEAPON_Y - 4)
    pygame.draw.rect(WIN, constants.WEAPONS, rect)
    WIN.blit(font.render('Lead Pipe', True, constants.BLACK), (53, 310))

    # Wrench
    background = pygame.Rect(175, 300, constants.WEAPON_X, constants.WEAPON_Y)
    pygame.draw.rect(WIN, constants.BLACK, background)
    rect = pygame.Rect(177, 302, constants.WEAPON_X - 4, constants.WEAPON_Y - 4)
    pygame.draw.rect(WIN, constants.WEAPONS, rect)
    WIN.blit(font.render('Wrench', True, constants.BLACK), (213, 310))


def make_suggestion(character, notes, room):
    char = None
    weapon = None

    font = pygame.font.SysFont('freesansbold.ttf', 26)

    selection = False
    while not selection:
        WIN.fill(constants.BACKGROUND)
        draw_suggestion(character, notes)

        # Displays choices to the user
        WIN.blit(font.render('Character: ', True, constants.BLACK), (25, 400))
        if char:
            WIN.blit(font.render(f'{char}', True, constants.BLACK), (120, 400))

        WIN.blit(font.render('Weapon: ', True, constants.BLACK), (25, 450))
        if weapon:
            WIN.blit(font.render(f'{weapon}', True, constants.BLACK), (100, 450))

        WIN.blit(font.render(f'Room: {room}', True, constants.BLACK), (25, 500))

        if weapon and char:
            # Confirmation button
            background = pygame.Rect(400, 400, constants.BUTTON_SIZE_X, constants.BUTTON_SIZE_Y)
            pygame.draw.rect(WIN, constants.BLACK, background)
            rect = pygame.Rect(402, 402, constants.BUTTON_SIZE_X - 4, constants.BUTTON_SIZE_Y - 4)
            pygame.draw.rect(WIN, constants.GREEN, rect)
            WIN.blit(font.render('Confirm', True, constants.BLACK), (417, 407))

        # Check for button clicks
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()

                # Characters - Colonel Mustard
                if 25 <= x <= 25 + constants.CHARACTER_X and 100 <= y <= 100 + constants.CHARACTER_Y:
                    char = 'Colonel Mustard'
                elif 175 <= x <= 175 + constants.CHARACTER_X and 100 <= y <= 100 + constants.CHARACTER_Y:
                    char = 'Miss Scarlet'
                elif 325 <= x <= 325 + constants.CHARACTER_X and 100 <= y <= 100 + constants.CHARACTER_Y:
                    char = 'Mrs. White'
                elif 475 <= x <= 475 + constants.CHARACTER_X and 100 <= y <= 100 + constants.CHARACTER_Y:
                    char = 'Reverend Green'
                elif 25 <= x <= 25 + constants.CHARACTER_X and 150 <= y <= 150 + constants.CHARACTER_Y:
                    char = 'Mr. Peacock'
                elif 175 <= x <= 175 + constants.CHARACTER_X and 150 <= y <= 150 + constants.CHARACTER_Y:
                    char = 'Professor Plum'
                elif 25 <= x <= 25 + constants.WEAPON_X and 250 <= y <= 250 + constants.WEAPON_Y:
                    weapon = 'Knife'
                elif 175 <= x <= 175 + constants.WEAPON_X and 250 <= y <= 250 + constants.WEAPON_Y:
                    weapon = 'Candle stick'
                elif 325 <= x <= 325 + constants.WEAPON_X and 250 <= y <= 250 + constants.WEAPON_Y:
                    weapon = 'Revolver'
                elif 475 <= x <= 475 + constants.WEAPON_X and 250 <= y <= 250 + constants.WEAPON_Y:
                    weapon = 'Rope'
                elif 25 <= x <= 25 + constants.WEAPON_X and 300 <= y <= 300 + constants.WEAPON_Y:
                    weapon = 'Lead pipe'
                elif 175 <= x <= 175 + constants.WEAPON_X and 300 <= y <= 300 + constants.WEAPON_Y:
                    weapon = 'Wrench'
                elif 400 <= x <= 400 + constants.BUTTON_SIZE_X and 400 <= y <= 400 + constants.BUTTON_SIZE_Y:
                    if weapon and char:
                        selection = True

        pygame.display.update()

    n.send(f'make_suggestion {character.value},{char},{weapon},{room}')
    ready = n.send('check_suggestion_status')
    title = pygame.font.SysFont('freesansbold.ttf', 30)

    while ready:
        c = n.send('waiting_on')
        WIN.blit(title.render(f'Waiting on {c.get_character().value} to respond', True, constants.BLACK), (100, 700))
        pygame.display.update()
        time.sleep(1)
        ready = n.send('check_suggestion_status')

    # Get response
    c = n.send('waiting_on')
    response = n.send('get_suggestion_response')
    WIN.blit(title.render(f'{c.get_character().value} shows you {response}', True, constants.BLACK), (100, 650))

    # Add this to players notes
    if response != 'No one could disprove':
        n.send(f'add_note {character.value},{response}')

    log.append(f'{c.get_character().value} shows you {response}')


def draw_related_cards(related_cards) -> {str: (int, int)}:
    title = pygame.font.SysFont('freesansbold.ttf', 40)
    font = pygame.font.SysFont('freesansbold.ttf', 26)
    WIN.blit(title.render('Related Cards: Pick one to show', True, constants.BLACK), (300, 100))
    related_map = {}

    if len(related_cards) > 0:
        for i, card in enumerate(related_cards):
            x = 100 + (i * 200)
            y = 175

            # Card background
            rect = pygame.Rect(x, y, 2 * constants.CARD_SIZE_X,  2 * constants.CARD_SIZE_Y)
            pygame.draw.rect(WIN, constants.BLACK, rect)
            rect = pygame.Rect(x+2, y+2, (2 * constants.CARD_SIZE_X) - 4, (2 * constants.CARD_SIZE_Y) - 4)
            pygame.draw.rect(WIN, constants.CARD, rect)

            # Card text
            card_value = card.get_value()
            related_map[card_value] = (x, y)
            WIN.blit(font.render(f'{card_value}', True, constants.BLACK),
                     (x + 4 * (20 - len(card_value)), y + 13))

    else:
        WIN.blit(title.render('You have no related cards to show', True, constants.BLACK), (300, 200))

    return related_map


def respond_suggestion(cards):
    suggestion = n.send('get_last_suggestion')
    font = pygame.font.SysFont('freesansbold.ttf', 28)

    related_cards = []
    for card in cards:
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
        WIN.fill(constants.BACKGROUND)
        related_map = draw_related_cards(related_cards)
        WIN.blit(font.render(f'You have selected: {card_choice}', True, constants.BLACK), (50, 322))

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
                if 400 <= x <= 400 + 2*constants.BUTTON_SIZE_X and 300 <= y <= 300 + 2*constants.BUTTON_SIZE_Y:
                    confirm = True

        if len(related_cards) == 0 or card_choice:
            # Confirmation button
            background = pygame.Rect(400, 300, 2 * constants.BUTTON_SIZE_X, 2 * constants.BUTTON_SIZE_Y)
            pygame.draw.rect(WIN, constants.BLACK, background)
            rect = pygame.Rect(402, 302, 2 * constants.BUTTON_SIZE_X - 4, 2 * constants.BUTTON_SIZE_Y - 4)
            pygame.draw.rect(WIN, constants.GREEN, rect)
            WIN.blit(font.render('Confirm', True, constants.BLACK), (460, 322))

        pygame.display.update()

    if card_choice:
        n.send(f'answer_suggestion {card_choice}')
    else:
        n.send('next_player')


def draw_accusation(character, notes):
    WIN.fill(constants.BACKGROUND)
    draw_suggestion(character, notes)

    title = pygame.font.SysFont('freesansbold.ttf', 30)
    font = pygame.font.SysFont('freesansbold.ttf', 20)

    # For accusations, we also include the rooms to choose from
    WIN.blit(title.render('Select a room', True, constants.BLACK), (25, 375))
    # Rooms - Hall
    background = pygame.Rect(25, 400, constants.ROOM_X, constants.ROOM_Y)
    pygame.draw.rect(WIN, constants.BLACK, background)
    rect = pygame.Rect(27, 402, constants.ROOM_X - 4, constants.ROOM_Y - 4)
    pygame.draw.rect(WIN, constants.HALL, rect)
    WIN.blit(font.render('Hall', True, constants.BLACK), (70, 410))

    # Lounge
    background = pygame.Rect(175, 400, constants.ROOM_X, constants.ROOM_Y)
    pygame.draw.rect(WIN, constants.BLACK, background)
    rect = pygame.Rect(177, 402, constants.ROOM_X - 4, constants.ROOM_Y - 4)
    pygame.draw.rect(WIN, constants.LOUNGE, rect)
    WIN.blit(font.render('Lounge', True, constants.BLACK), (215, 410))

    # Dining Room
    background = pygame.Rect(325, 400, constants.ROOM_X, constants.ROOM_Y)
    pygame.draw.rect(WIN, constants.BLACK, background)
    rect = pygame.Rect(327, 402, constants.ROOM_X - 4, constants.ROOM_Y - 4)
    pygame.draw.rect(WIN, constants.DINING, rect)
    WIN.blit(font.render('Dining Room', True, constants.BLACK), (345, 410))

    # Kitchen
    background = pygame.Rect(475, 400, constants.ROOM_X, constants.ROOM_Y)
    pygame.draw.rect(WIN, constants.BLACK, background)
    rect = pygame.Rect(477, 402, constants.ROOM_X - 4, constants.ROOM_Y - 4)
    pygame.draw.rect(WIN, constants.KITCHEN, rect)
    WIN.blit(font.render('Kitchen', True, constants.BLACK), (514, 410))

    # Ballroom
    background = pygame.Rect(25, 450, constants.ROOM_X, constants.ROOM_Y)
    pygame.draw.rect(WIN, constants.BLACK, background)
    rect = pygame.Rect(27, 452, constants.ROOM_X - 4, constants.ROOM_Y - 4)
    pygame.draw.rect(WIN, constants.BALL, rect)
    WIN.blit(font.render('Ballroom', True, constants.BLACK), (57, 460))

    # Conservatory
    background = pygame.Rect(175, 450, constants.ROOM_X, constants.ROOM_Y)
    pygame.draw.rect(WIN, constants.BLACK, background)
    rect = pygame.Rect(177, 452, constants.ROOM_X - 4, constants.ROOM_Y - 4)
    pygame.draw.rect(WIN, constants.CONSERVATORY, rect)
    WIN.blit(font.render('Conservatory', True, constants.BLACK), (196, 460))

    # Billiard Room
    background = pygame.Rect(325, 450, constants.ROOM_X, constants.ROOM_Y)
    pygame.draw.rect(WIN, constants.BLACK, background)
    rect = pygame.Rect(327, 452, constants.ROOM_X - 4, constants.ROOM_Y - 4)
    pygame.draw.rect(WIN, constants.BILLIARDS, rect)
    WIN.blit(font.render('Billiard Room', True, constants.BLACK), (345, 460))

    # Library
    background = pygame.Rect(475, 450, constants.ROOM_X, constants.ROOM_Y)
    pygame.draw.rect(WIN, constants.BLACK, background)
    rect = pygame.Rect(477, 452, constants.ROOM_X - 4, constants.ROOM_Y - 4)
    pygame.draw.rect(WIN, constants.LIBRARY, rect)
    WIN.blit(font.render('Library', True, constants.BLACK), (517, 460))

    # Study
    background = pygame.Rect(25, 500, constants.ROOM_X, constants.ROOM_Y)
    pygame.draw.rect(WIN, constants.BLACK, background)
    rect = pygame.Rect(27, 502, constants.ROOM_X - 4, constants.ROOM_Y - 4)
    pygame.draw.rect(WIN, constants.STUDY, rect)
    WIN.blit(font.render('Study', True, constants.BLACK), (65, 510))


def handle_accusation(character, notes):
    char = None
    weapon = None
    room = None

    confirm = False
    flag = False

    title = pygame.font.SysFont('freesansbold.ttf', 36)
    font = pygame.font.SysFont('freesansbold.ttf', 24)

    while not flag:
        draw_accusation(character, notes)

        # Section title
        WIN.blit(title.render('Make an Accusation', True, constants.BLACK), (250, 40))

        # Displays choices to the user
        WIN.blit(font.render('Character: ', True, constants.BLACK), (25, 600))
        if char:
            WIN.blit(font.render(f'{char}', True, constants.BLACK), (120, 600))

        WIN.blit(font.render('Weapon: ', True, constants.BLACK), (275, 600))
        if weapon:
            WIN.blit(font.render(f'{weapon}', True, constants.BLACK), (350, 600))

        WIN.blit(font.render(f'Room: ', True, constants.BLACK), (480, 600))
        if room:
            WIN.blit(font.render(f'{room}', True, constants.BLACK), (540, 600))

        # Confirm button
        background = pygame.Rect(175, 650, constants.ROOM_X, constants.ROOM_Y)
        pygame.draw.rect(WIN, constants.BLACK, background)
        rect = pygame.Rect(177, 652, constants.ROOM_X - 4, constants.ROOM_Y - 4)
        pygame.draw.rect(WIN, constants.GREEN, rect)
        WIN.blit(font.render('Confirm', True, constants.BLACK), (207, 658))

        # Cancel button
        background = pygame.Rect(325, 650, constants.ROOM_X, constants.ROOM_Y)
        pygame.draw.rect(WIN, constants.BLACK, background)
        rect = pygame.Rect(327, 652, constants.ROOM_X - 4, constants.ROOM_Y - 4)
        pygame.draw.rect(WIN, constants.SCARLET, rect)
        WIN.blit(font.render('Cancel', True, constants.BLACK), (357, 658))

        # Check for button clicks
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()

                # Characters - Colonel Mustard
                if 25 <= x <= 25 + constants.CHARACTER_X and 100 <= y <= 100 + constants.CHARACTER_Y:
                    char = 'Colonel Mustard'
                elif 175 <= x <= 175 + constants.CHARACTER_X and 100 <= y <= 100 + constants.CHARACTER_Y:
                    char = 'Miss Scarlet'
                elif 325 <= x <= 325 + constants.CHARACTER_X and 100 <= y <= 100 + constants.CHARACTER_Y:
                    char = 'Mrs. White'
                elif 475 <= x <= 475 + constants.CHARACTER_X and 100 <= y <= 100 + constants.CHARACTER_Y:
                    char = 'Reverend Green'
                elif 25 <= x <= 25 + constants.CHARACTER_X and 150 <= y <= 150 + constants.CHARACTER_Y:
                    char = 'Mr. Peacock'
                elif 175 <= x <= 175 + constants.CHARACTER_X and 150 <= y <= 150 + constants.CHARACTER_Y:
                    char = 'Professor Plum'
                elif 25 <= x <= 25 + constants.WEAPON_X and 250 <= y <= 250 + constants.WEAPON_Y:
                    weapon = 'Knife'
                elif 175 <= x <= 175 + constants.WEAPON_X and 250 <= y <= 250 + constants.WEAPON_Y:
                    weapon = 'Candle stick'
                elif 325 <= x <= 325 + constants.WEAPON_X and 250 <= y <= 250 + constants.WEAPON_Y:
                    weapon = 'Revolver'
                elif 475 <= x <= 475 + constants.WEAPON_X and 250 <= y <= 250 + constants.WEAPON_Y:
                    weapon = 'Rope'
                elif 25 <= x <= 25 + constants.WEAPON_X and 300 <= y <= 300 + constants.WEAPON_Y:
                    weapon = 'Lead pipe'
                elif 175 <= x <= 175 + constants.WEAPON_X and 300 <= y <= 300 + constants.WEAPON_Y:
                    weapon = 'Wrench'
                elif 25 <= x <= 25 + constants.ROOM_X and 400 <= y <= 400 + constants.ROOM_Y:
                    room = 'Hall'
                elif 175 <= x <= 175 + constants.ROOM_X and 400 <= y <= 400 + constants.ROOM_Y:
                    room = 'Lounge'
                elif 325 <= x <= 325 + constants.ROOM_X and 400 <= y <= 400 + constants.ROOM_Y:
                    room = 'Dining Room'
                elif 475 <= x <= 475 + constants.ROOM_X and 400 <= y <= 400 + constants.ROOM_Y:
                    room = 'Kitchen'
                elif 25 <= x <= 25 + constants.ROOM_X and 450 <= y <= 450 + constants.ROOM_Y:
                    room = 'Ballroom'
                elif 175 <= x <= 175 + constants.ROOM_X and 450 <= y <= 450 + constants.ROOM_Y:
                    room = 'Conservatory'
                elif 325 <= x <= 325 + constants.ROOM_X and 450 <= y <= 450 + constants.ROOM_Y:
                    room = 'Billiard Room'
                elif 475 <= x <= 475 + constants.ROOM_X and 450 <= y <= 450 + constants.ROOM_Y:
                    room = 'Library'
                elif 25 <= x <= 25 + constants.ROOM_X and 500 <= y <= 500 + constants.ROOM_Y:
                    room = 'Study'

                # Confirm button
                elif 175 <= x <= 175 + constants.ROOM_X and 650 <= y <= 650 + constants.ROOM_Y:
                    if character and weapon and room:
                        confirm = True
                        flag = True

                # Cancel button
                elif 325 <= x <= 325 + constants.ROOM_X and 650 <= y <= 650 + constants.ROOM_Y:
                    flag = True

        pygame.display.update()

    if flag and confirm:
        # Send the accusation to the server
        n.send(f'make_accusation {character.value},{char},{weapon},{room}')
    else:
        # Cancel button was pressed
        return 'Cancelled'


def handle_turn(board, cards, character, notes, player_positions, current_turn) -> {str: int}:
    draw_screen(board, cards, character, notes, player_positions, current_turn)
    pygame.display.update()

    populate_rooms(board, player_positions)
    room = board.what_room(player_positions[character.value])

    # TODO: If you enter a room you can also make a suggestion when you pick rolling dice
    if room not in ['Hallway', 'OFB', 'Start']:
        # Allow them to choose to move, make a suggestion, use a passageway, or make an accusation
        choice = draw_buttons(room)

        if choice == 'Move':
            # Free the position in the room
            free_position(board, room, player_positions[character.value])

            # If there's multiple exits, let the player choose which one they want to leave from
            if len(constants.ENTRANCES[room]) > 1:
                player_positions[character.value] = pick_exit(board, room)
            else:
                player_positions[character.value] = constants.ENTRANCES[room][0]

            roll_dice(board, cards, character, notes, player_positions, current_turn, True)

        elif choice == 'Suggestion':
            make_suggestion(character, notes, room)

        elif choice == 'Accusation':
            status = handle_accusation(character, notes)
            if status and status == 'Cancelled':
                return handle_turn(board, cards, character, notes, player_positions, current_turn)

        elif choice == 'Passage':
            if room == 'Kitchen':
                player_positions[character.value] = constants.ENTRANCES['Study'][0]
            elif room == 'Study':
                player_positions[character.value] = constants.ENTRANCES['Kitchen'][0]
            elif room == 'Conservatory':
                player_positions[character.value] = constants.ENTRANCES['Lounge'][0]
            elif room == 'Lounge':
                player_positions[character.value] = constants.ENTRANCES['Conservatory'][0]

            player_positions[character.value] = give_room_position(board, player_positions[character.value])

    else:
        player_positions = roll_dice(board, cards, character, notes, player_positions, current_turn, False)

    return player_positions


def draw_disqualification():
    font = pygame.font.SysFont('freesansbold.ttf', 20)
    WIN.blit(font.render('You have been disqualified', True, constants.SCARLET), (700, 430))
    WIN.blit(font.render('You have lost your turn, but still must answer suggestions', True, constants.BLACK),
             (610, 450))


def main():
    selected = None
    valid = False
    ready = False
    game_finished = False
    previous_turn = 0

    # Make sure that the choice selected by the user is valid
    print("Selecting character...")
    while not valid:
        selected = select_character()
        valid = n.send(selected.value)

    print("Creating player...")

    # How to wait for the start
    while not ready:
        show_ready()
        pygame.display.update()
        ready = n.send('start')

    print("Starting game...")
    board = Board(WIN)

    print("Getting cards...")
    cards = n.send(f'get_cards {selected.value}')

    current_turn = n.send('whos_turn')
    player_positions = n.send('get_all_positions')

    disqualified = False

    while not game_finished:
        # Ask whose turn it is
        turn_num = n.send('turn')
        notes = n.send(f'get_notes {selected.value}')

        # If a player has moved, then get the positions of all players
        if turn_num != previous_turn:
            current_turn = n.send('whos_turn')
            previous_turn = current_turn
            player_positions = n.send('get_all_positions')

        # Draw the board
        draw_screen(board, cards, selected, notes, player_positions, current_turn)

        # Handle our turn
        if current_turn.get_character().value == selected.value:
            if not disqualified:
                player_positions = handle_turn(board, cards, selected, notes, player_positions, current_turn)
                draw_screen(board, cards, selected, notes, player_positions, current_turn)
                n.send(f'update_position {selected.value},{player_positions[selected.value]}')
            n.send('turn_done')

        # If it's not our turn, check for a suggestion
        if not current_turn.get_character().value == selected.value:
            waiting_on = n.send('waiting_on')
            pending_suggestion = n.send('check_suggestion_status')

            if pending_suggestion is True and (waiting_on and waiting_on.get_character() == selected):
                print("You have a suggestion to respond to...")
                respond_suggestion(cards)

        # Check if our player is disqualified from the match
        if not disqualified:
            disqualified = n.send(f'check_disqualified {selected.value}')

        if disqualified:
            draw_disqualification()

        pygame.display.update()

        game_finished = n.send('game_finished')
        if game_finished:
            # End game screen
            pass


main()
