import constants
import pygame
import random
import sys
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
    draw_log()


def draw_log():
    """
    Log that displays recent actions of players to other players
    :return: None
    """
    add_to_log()

    global log
    if len(log) <= 6:
        these_logs = log
    else:
        these_logs = log[len(log) - 6:]

    draw_text('LOG', 22, constants.BLACK, 775, 550)
    draw_box(630, 565, constants.LOG_X, constants.LOG_Y, constants.LOG)

    for i, line in enumerate(these_logs):
        x = 636
        y = 573 + (i * 20)

        if len(line) <= 50:
            draw_text(line, 16, constants.WHITE, x, y)
        else:
            draw_text(line, 14, constants.WHITE, x, y)


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
    draw_text(f"It's {player.get_character().value}'s turn", 24, constants.BLACK, 700, 725)


def draw_moves(move):
    """
    Draws an indicator that tells the player how many moves they have left
    :param move: Integer of how many moves are left
    :return: Nothing
    """
    draw_text(f'You have {move} moves left', 24, constants.SCARLET, 700, 700)


def draw_notes(name, notes):
    """
    Draws information that tells the player what they already know in relation to the murder mystery
    :param name: Characters name (str)
    :param notes: Information this player knows (arr length 3) Index 0: characters, Index 1: weapons, Index 2: locations
    :return: Nothing
    """
    font = pygame.font.SysFont('freesansbold.ttf', 20)
    draw_text(f"{name}'s notes", 32, constants.BLACK, 675, 30)
    all_cards = Deck.all_values()

    # Characters
    draw_text("Potential Murder Suspects", 24, constants.BLACK, 675, 75)
    for i, character in enumerate(all_cards[0]):
        x = 675 + (i//3 * 125)
        y = 100 + ((i % 3) * 20)
        WIN.blit(font.render(f"{character}", True, constants.BLACK), (x, y))

        if character in notes[0]:
            pygame.draw.line(WIN, constants.BLACK, (x, y+6), (x + len(character)*7, y+6), 2)

    # Weapons
    draw_text("Potential Murder Weapons", 24, constants.BLACK, 675, 200)
    for i, weapon in enumerate(all_cards[1]):
        x = 675 + (i//3 * 125)
        y = 225 + ((i % 3) * 20)

        WIN.blit(font.render(f"{weapon}", True, constants.BLACK), (x, y))

        if weapon in notes[1]:
            pygame.draw.line(WIN, constants.BLACK, (x, y + 6), (x + len(weapon)*7, y + 6), 2)

    # Locations
    draw_text("Potential Murder Locations", 24, constants.BLACK, 675, 325)
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
    font = pygame.font.SysFont('freesansbold.ttf', 14)
    draw_text('Your cards', 20, constants.BLACK, 265, 635)

    for i, card in enumerate(cards):
        x = 10 + ((i % 6) * 100)
        y = 655 + (30 * (i // 6))

        # Card background
        draw_box(x, y, constants.CARD_SIZE_X, constants.CARD_SIZE_Y, constants.CARD)
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
        draw_text(f'{num_ready[1]} out of {num_ready[0]} players ready', 26, constants.BLACK, 50, 50)

        # Fonts
        font2 = pygame.font.SysFont('freesansbold.ttf', 26)

        draw_text('Select a Character', 60, constants.BLACK, 300, 200)

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

            draw_box(x, y, constants.CHARACTER_SELECTION_SIZE, constants.CHARACTER_SELECTION_SIZE, color)
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
        draw_text('Character Selected: ', 32, constants.BLACK, 300, 500)

        # If a choice has been made, add a confirmation button to create the player
        if choice:
            draw_text(choice.value, 32, constants.BLACK, 550, 500)

        # Button to confirm selection (will confirm the selection made if choice != None
        draw_box(425, 600, 125, 65, constants.GREEN)
        draw_text('Confirm', 32, constants.BLACK, 442, 622)
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
    draw_text(f'Select an exit from {room} by clicking on it', 24, constants.SCARLET, 630, 700)

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
    """
    Allows client to make a choice of what they want to do during their turn
    :param room: String representing the room the player is in, used for secret passageways
    :return: String representing the choice the user selected
    """
    choice = ''

    # Roll Dice button
    draw_box(630, 455, constants.BUTTON_SIZE_X, constants.BUTTON_SIZE_Y, constants.ROLL_DICE)
    draw_text('Roll Dice', 22, constants.BLACK, 647, 463)

    # Suggestion button
    draw_box(655 + constants.BUTTON_SIZE_X, 455, constants.BUTTON_SIZE_X, constants.BUTTON_SIZE_Y, constants.SUGGESTION)
    draw_text('Suggestion', 22, constants.BLACK, 663 + constants.BUTTON_SIZE_X, 463)

    # Accusation
    draw_box(680 + 2 * constants.BUTTON_SIZE_X, 455, constants.BUTTON_SIZE_X, constants.BUTTON_SIZE_Y,
             constants.SCARLET)
    draw_text('Accusation', 22, constants.BLACK, 688 + 2 * constants.BUTTON_SIZE_X, 463)

    # Passage way
    if room in ['Kitchen', 'Lounge', 'Conservatory', 'Study']:
        draw_box(630, 480 + constants.BUTTON_SIZE_Y, constants.BUTTON_SIZE_X, constants.BUTTON_SIZE_Y,
                 constants.PASSAGE)
        draw_text('Passage', 18, constants.BLACK, 655, 514)

        if room == 'Kitchen':
            draw_text('To Study', 18, constants.BLACK, 655, 525)
        elif room == 'Study':
            draw_text('To Kitchen', 18, constants.BLACK, 648, 525)
        elif room == 'Conservatory':
            draw_text('To Lounge', 18, constants.BLACK, 650, 525)
        elif room == 'Lounge':
            draw_text('To Conservatory', 18, constants.BLACK, 633, 525)

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


def suggest_or_pass(character, notes, room):
    """
    When a player enters a room, they need to have the option to make an accusation
    :param character: Character enum representing the player's character
    :param notes: Array of arrays of strings representing information the player knows
    :param room: String of what room the player is located in
    :return: None
    """

    # Suggestion
    draw_box(630, 455, constants.BUTTON_SIZE_X, constants.BUTTON_SIZE_Y, constants.SUGGESTION)
    draw_text('Suggestion', 22, constants.BLACK, 639, 463)

    # Pass
    draw_box(655 + constants.BUTTON_SIZE_X, 455, constants.BUTTON_SIZE_X, constants.BUTTON_SIZE_Y, constants.SCARLET)
    draw_text('Pass', 22, constants.BLACK, 688 + constants.BUTTON_SIZE_X, 463)

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

    pygame.event.clear()

    if choice == 'Suggestion':
        make_suggestion(character, notes, room)


def accusation_or_pass(character, notes):
    """
    When a player does not receive an answer to a suggestion, they may make an accusation
    :param character: Character enum representing the player's character
    :param notes: Array of arrays of strings representing information the player knows
    :return: None
    """

    # Title
    draw_text('No one could disprove your suggestion', 22, constants.SCARLET, 600, 495)
    draw_text('Would you like to make an accusation?', 22, constants.BLACK, 600, 515)

    # Accusation
    draw_box(630, 455, constants.BUTTON_SIZE_X, constants.BUTTON_SIZE_Y, constants.SCARLET)
    draw_text('Accusation', 22, constants.BLACK, 639, 463)

    # Pass
    draw_box(655 + constants.BUTTON_SIZE_X, 455, constants.BUTTON_SIZE_X, constants.BUTTON_SIZE_Y, constants.PASSAGE)
    draw_text('Pass', 22, constants.BLACK, 688 + constants.BUTTON_SIZE_X, 463)

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
                    choice = 'Accusation'
                elif 655 + constants.BUTTON_SIZE_X <= x <= 655 + 2 * constants.BUTTON_SIZE_X and \
                        455 <= y <= 455 + constants.BUTTON_SIZE_Y:
                    choice = 'Pass'

    pygame.event.clear()

    if choice == 'Accusation':
        handle_accusation(character, notes)


def roll_dice(board, cards, character, notes, player_positions, current_turn, exiting) -> {str: int}:
    """
    Simulates a double dice roll and handles the movement
    :param board: Board object
    :param cards: Array of Card objects
    :param character: Character enum
    :param notes: Array of arrays of strings
    :param player_positions: Dictionary mapping {characters name (str) -> position on board (int)}
    :param current_turn: String representing whose turn it is
    :param exiting: Boolean of if the player is leaving a room or not
    :return: Dictionary mapping {characters name (str) -> position on board (int)}
    """
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
            suggest_or_pass(character, notes, board.what_room(player_positions[character.value]))

        draw_screen(board, cards, character, notes, player_positions, current_turn)
        draw_moves(moves)
        pygame.display.update()

    return player_positions


def draw_suggestion(character, notes):
    """
    Draws the screen for suggestions
    :param character: Character enum
    :param notes: Array of arrays of strings
    :return: None
    """
    draw_notes(character.value, notes)
    font = pygame.font.SysFont('freesansbold.ttf', 20)

    draw_text('Select a character', 30, constants.BLACK, 25, 75)
    # Characters - Colonel Mustard
    draw_box(25, 100, constants.CHARACTER_X, constants.CHARACTER_Y, constants.MUSTARD)
    WIN.blit(font.render('Colonel Mustard', True, constants.BLACK), (36, 110))

    # Miss Scarlet
    draw_box(175, 100, constants.CHARACTER_X, constants.CHARACTER_Y, constants.SCARLET)
    WIN.blit(font.render('Miss Scarlet', True, constants.BLACK), (198, 110))

    # Mrs. White
    draw_box(325, 100, constants.CHARACTER_X, constants.CHARACTER_Y, constants.WHITE)
    WIN.blit(font.render('Mrs. White', True, constants.BLACK), (353, 110))

    # Reverend Green
    draw_box(475, 100, constants.CHARACTER_X, constants.CHARACTER_Y, constants.GREEN)
    WIN.blit(font.render('Reverend Green', True, constants.BLACK), (485, 110))

    # Mr. Peacock
    draw_box(25, 150, constants.CHARACTER_X, constants.CHARACTER_Y, constants.PEACOCK)
    WIN.blit(font.render('Mr. Peacock', True, constants.BLACK), (50, 160))

    # Professor Plum
    draw_box(175, 150, constants.CHARACTER_X, constants.CHARACTER_Y, constants.PLUM)
    WIN.blit(font.render('Professor Plum', True, constants.BLACK), (188, 160))

    draw_text('Select a weapon', 30, constants.BLACK, 25, 225)
    # Weapons - Knife
    draw_box(25, 250, constants.WEAPON_X, constants.WEAPON_Y, constants.WEAPONS)
    WIN.blit(font.render('Knife', True, constants.BLACK), (70, 260))

    # Candle stick
    draw_box(175, 250, constants.WEAPON_X, constants.WEAPON_Y, constants.WEAPONS)
    WIN.blit(font.render('Candle stick', True, constants.BLACK), (196, 260))

    # Revolver
    draw_box(325, 250, constants.WEAPON_X, constants.WEAPON_Y, constants.WEAPONS)
    WIN.blit(font.render('Revolver', True, constants.BLACK), (357, 260))

    # Rope
    draw_box(475, 250, constants.WEAPON_X, constants.WEAPON_Y, constants.WEAPONS)
    WIN.blit(font.render('Rope', True, constants.BLACK), (517, 260))

    # Lead Pipe
    draw_box(25, 300, constants.WEAPON_X, constants.WEAPON_Y, constants.WEAPONS)
    WIN.blit(font.render('Lead Pipe', True, constants.BLACK), (53, 310))

    # Wrench
    draw_box(175, 300, constants.WEAPON_X, constants.WEAPON_Y, constants.WEAPONS)
    WIN.blit(font.render('Wrench', True, constants.BLACK), (213, 310))


def make_suggestion(character, notes, room) -> str:
    """
    Handles selection for suggestions, tells suggestion to the server and waits for a response
    :param character: Character enum
    :param notes: Array of arrays of strings
    :param room: String representing room player is in
    :return: Optional string
    """
    char = None
    weapon = None

    font = pygame.font.SysFont('freesansbold.ttf', 26)

    confirm = False
    run = True
    while run:
        WIN.fill(constants.BACKGROUND)
        draw_suggestion(character, notes)

        # Displays choices to the user
        WIN.blit(font.render('Character: ', True, constants.BLACK), (25, 400))
        if char:
            WIN.blit(font.render(f'{char}', True, constants.BLACK), (120, 400))

        WIN.blit(font.render('Weapon: ', True, constants.BLACK), (275, 400))
        if weapon:
            WIN.blit(font.render(f'{weapon}', True, constants.BLACK), (350, 400))

        WIN.blit(font.render(f'Room: {room}', True, constants.BLACK), (25, 450))

        # Confirm button
        draw_box(175, 675, constants.ROOM_X, constants.ROOM_Y, constants.GREEN)
        WIN.blit(font.render('Confirm', True, constants.BLACK), (207, 683))

        # Cancel button
        draw_box(325, 675, constants.ROOM_X, constants.ROOM_Y, constants.SCARLET)
        WIN.blit(font.render('Cancel', True, constants.BLACK), (357, 683))

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
                    char = 'Mrs.White'
                elif 475 <= x <= 475 + constants.CHARACTER_X and 100 <= y <= 100 + constants.CHARACTER_Y:
                    char = 'Reverend Green'
                elif 25 <= x <= 25 + constants.CHARACTER_X and 150 <= y <= 150 + constants.CHARACTER_Y:
                    char = 'Mr.Peacock'
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
                elif 175 <= x <= 175 + constants.ROOM_X and 675 <= y <= 675 + constants.ROOM_Y:
                    if weapon and char:
                        confirm = True
                        run = False
                elif 325 <= x <= 325 + constants.ROOM_X and 675 <= y <= 675 + constants.ROOM_Y:
                    run = False

        pygame.display.update()

    if confirm:
        n.send(f'make_suggestion {char},{weapon},{room}')
        ready = n.send('check_suggestion_status')
        title = pygame.font.SysFont('freesansbold.ttf', 30)

        while ready:
            c = n.send('waiting_on')
            WIN.blit(title.render(f'Waiting on {c.get_character().value} to respond', True, constants.BLACK),
                     (25, 725))
            pygame.display.update()
            time.sleep(1)
            ready = n.send('check_suggestion_status')

        # Get response
        c = n.send('waiting_on')
        response = n.send('get_suggestion_response')

        # Add this to players notes
        add_to_log()

        if response != 'No one could disprove':
            n.send(f'add_note {response}')
            log.append(f'{c.get_character().value} shows you {response}')
        else:
            accusation_or_pass(character, notes)
            log.append(response)

    # Cancel button was pressed
    else:
        return 'Cancelled'


def draw_related_cards(related_cards) -> {str: (int, int)}:
    """
    Draws cards for answering suggestions
    :param related_cards: Array of card objects
    :return: Dictionary mapping {card value (str) -> (x , y) positions (int, int)}
    """
    font = pygame.font.SysFont('freesansbold.ttf', 26)
    draw_text('Related Cards: Pick one to show', 40, constants.BLACK, 300, 100)
    related_map = {}

    if len(related_cards) > 0:
        for i, card in enumerate(related_cards):
            x = 100 + (i * 200)
            y = 175

            # Card background
            draw_box(x, y, 2 * constants.CARD_SIZE_X, 2 * constants.CARD_SIZE_Y, constants.CARD)

            # Card text
            card_value = card.get_value()
            related_map[card_value] = (x, y)
            WIN.blit(font.render(f'{card_value}', True, constants.BLACK),
                     (x + 4 * (20 - len(card_value)), y + 13))

    else:
        draw_text('You have no related cards to show', 40, constants.BLACK, 300, 200)

    return related_map


def respond_suggestion(cards):
    """
    Handles the choice of card to show during a suggestion
    :param cards: Array of card objects
    :return: None
    """
    suggestion = n.send('get_last_suggestion')

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
        draw_text(f'You have selected: {card_choice}', 28, constants.BLACK, 50, 322)

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
            draw_box(400, 300, 2 * constants.BUTTON_SIZE_X, 2 * constants.BUTTON_SIZE_Y, constants.GREEN)
            draw_text('Confirm', 28, constants.BLACK, 460, 322)

        pygame.display.update()

    if card_choice:
        n.send(f'answer_suggestion {card_choice}')
    else:
        n.send('next_player')


def draw_accusation(character, notes):
    """
    Draws the screen for accusations
    :param character: Character enum
    :param notes: Array of arrays of strings
    :return: None
    """
    WIN.fill(constants.BACKGROUND)
    draw_suggestion(character, notes)
    font = pygame.font.SysFont('freesansbold.ttf', 20)

    # For accusations, we also include the rooms to choose from
    draw_text('Select a room', 30, constants.BLACK, 25, 375)
    # Rooms - Hall
    draw_box(25, 400, constants.ROOM_X, constants.ROOM_Y, constants.HALL)
    WIN.blit(font.render('Hall', True, constants.BLACK), (70, 410))

    # Lounge
    draw_box(175, 400, constants.ROOM_X, constants.ROOM_Y, constants.LOUNGE)
    WIN.blit(font.render('Lounge', True, constants.BLACK), (215, 410))

    # Dining Room
    draw_box(325, 400, constants.ROOM_X, constants.ROOM_Y, constants.DINING)
    WIN.blit(font.render('Dining Room', True, constants.BLACK), (345, 410))

    # Kitchen
    draw_box(475, 400, constants.ROOM_X, constants.ROOM_Y, constants.KITCHEN)
    WIN.blit(font.render('Kitchen', True, constants.BLACK), (514, 410))

    # Ballroom
    draw_box(25, 450, constants.ROOM_X, constants.ROOM_Y, constants.BALL)
    WIN.blit(font.render('Ballroom', True, constants.BLACK), (57, 460))

    # Conservatory
    draw_box(175, 450, constants.ROOM_X, constants.ROOM_Y, constants.CONSERVATORY)
    WIN.blit(font.render('Conservatory', True, constants.BLACK), (196, 460))

    # Billiard Room
    draw_box(325, 450, constants.ROOM_X, constants.ROOM_Y, constants.BILLIARDS)
    WIN.blit(font.render('Billiard Room', True, constants.BLACK), (345, 460))

    # Library
    draw_box(475, 450, constants.ROOM_X, constants.ROOM_Y, constants.LIBRARY)
    WIN.blit(font.render('Library', True, constants.BLACK), (517, 460))

    # Study
    draw_box(25, 500, constants.ROOM_X, constants.ROOM_Y, constants.STUDY)
    WIN.blit(font.render('Study', True, constants.BLACK), (65, 510))


def handle_accusation(character, notes) -> str:
    """
    Handles selections for accusation, sends it into the server
    :param character: Character enum
    :param notes: Array of arrays of strings
    :return: Optional String
    """
    char = None
    weapon = None
    room = None

    confirm = False
    flag = False

    font = pygame.font.SysFont('freesansbold.ttf', 24)

    while not flag:
        draw_accusation(character, notes)

        # Section title
        draw_text('Make an Accusation', 36, constants.BLACK, 250, 40)

        # Displays choices to the user
        WIN.blit(font.render('Character: ', True, constants.BLACK), (25, 550))
        if char:
            WIN.blit(font.render(f'{char}', True, constants.BLACK), (120, 550))

        WIN.blit(font.render('Weapon: ', True, constants.BLACK), (275, 550))
        if weapon:
            WIN.blit(font.render(f'{weapon}', True, constants.BLACK), (350, 550))

        WIN.blit(font.render(f'Room: ', True, constants.BLACK), (480, 550))
        if room:
            WIN.blit(font.render(f'{room}', True, constants.BLACK), (540, 550))

        # Confirm button
        draw_box(175, 675, constants.ROOM_X, constants.ROOM_Y, constants.GREEN)
        WIN.blit(font.render('Confirm', True, constants.BLACK), (207, 683))

        # Cancel button
        draw_box(325, 675, constants.ROOM_X, constants.ROOM_Y, constants.SCARLET)
        WIN.blit(font.render('Cancel', True, constants.BLACK), (357, 683))

        # Disclaimer
        draw_text('WARNING', 36, constants.SCARLET, 725, 625)
        draw_text('An incorrect accusation leads to disqualification', 20, constants.BLACK, 625, 660)
        draw_text('You will lose your turns, and may only respond to suggestions', 20, constants.BLACK, 590, 690)

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
                    char = 'Mrs.White'
                elif 475 <= x <= 475 + constants.CHARACTER_X and 100 <= y <= 100 + constants.CHARACTER_Y:
                    char = 'Reverend Green'
                elif 25 <= x <= 25 + constants.CHARACTER_X and 150 <= y <= 150 + constants.CHARACTER_Y:
                    char = 'Mr.Peacock'
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
                elif 175 <= x <= 175 + constants.ROOM_X and 675 <= y <= 675 + constants.ROOM_Y:
                    if character and weapon and room:
                        confirm = True
                        flag = True

                # Cancel button
                elif 325 <= x <= 325 + constants.ROOM_X and 675 <= y <= 675 + constants.ROOM_Y:
                    flag = True

        pygame.display.update()

    if flag and confirm:
        # Send the accusation to the server
        n.send(f'make_accusation {char},{weapon},{room}')
    else:
        # Cancel button was pressed
        return 'Cancelled'


def handle_turn(board, cards, character, notes, player_positions, current_turn) -> {str: int}:
    """
    Primary function in charge of managing players turn
    :param board: Board object
    :param cards: Array of card objects
    :param character: Character Enum
    :param notes: Array of arrays of strings
    :param player_positions: Dictionary mapping players to their positions
    :param current_turn: String representing whose turn it is
    :return: Dictionary mapping players to their positions (updated with the players new position after their turn)
    """
    draw_screen(board, cards, character, notes, player_positions, current_turn)
    pygame.display.update()

    populate_rooms(board, player_positions)
    room = board.what_room(player_positions[character.value])

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
            status = make_suggestion(character, notes, room)
            if status == 'Cancelled':
                return handle_turn(board, cards, character, notes, player_positions, current_turn)

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
            draw_screen(board, cards, character, notes, player_positions, current_turn)
            room = board.what_room(player_positions[character.value])
            pygame.display.update()

            suggest_or_pass(character, notes, room)

    else:
        player_positions = roll_dice(board, cards, character, notes, player_positions, current_turn, False)

    return player_positions


def draw_disqualification():
    """
    Draws the disqualification message
    """
    draw_text('You have been disqualified', 20, constants.SCARLET, 700, 430)
    draw_text('You have lost your turn, but still must answer suggestions', 20, constants.BLACK, 610, 450)


def draw_end_screen(character):
    """
    Draws end game screen that displays the winner
    :param character: Character enum
    :return: None
    """
    winner = n.send('get_winner')
    run = True

    while run:
        WIN.fill(constants.BACKGROUND)

        # Winner title
        if winner == character.value:
            draw_text('Congratulations! You Won!', 60, constants.BLACK, 225, 100)
        elif not winner:
            draw_text('Everyone Disqualified! You Lose!', 60, constants.BLACK, 200, 100)
        else:
            draw_text(f'{winner} Won!', 60, constants.BLACK, 275 + 5 * (18 - len(winner)), 100)

        # Quit button
        draw_box(300, 300, 3 * constants.ROOM_X, 3 * constants.ROOM_Y, constants.GREEN)
        draw_text('Quit', 60, constants.BLACK, 435, 325)

        for event in pygame.event.get():
            # Force quit
            if event.type == pygame.QUIT:
                run = False

            # Quit button
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()

                if 300 <= x <= 300 + 3*constants.ROOM_X and 300 <= y <= 300 + 3*constants.ROOM_Y:
                    run = False

        pygame.display.update()


def add_to_log():
    """
    Updates and merges client personal log with the server log
    """
    global log
    server_log = n.send('get_log')

    for item in server_log:
        if item not in log:
            log.append(item)


def draw_box(x, y, x_length, y_length, color):
    """
    Draws a box on the window
    :param x: Integer, x position of top left corner
    :param y: Integer, y position of top left corner
    :param x_length: Integer, length
    :param y_length: Integer, height
    :param color: (int, int, int), color of box
    """

    background = pygame.Rect(x, y, x_length, y_length)
    pygame.draw.rect(WIN, constants.BLACK, background)
    rect = pygame.Rect(x + 2, y + 2, x_length - 4, y_length - 4)
    pygame.draw.rect(WIN, color, rect)


def draw_text(text, size, color, x, y):
    """
    Draws a text object on the window
    :param text: String, text being displayed
    :param size: Integer, size of the text
    :param color: (int, int, int), color of the text
    :param x: Integer, x position of top left corner
    :param y: Integer, y position of top left corner
    """
    font = pygame.font.SysFont('freesansbold.ttf', size)
    WIN.blit(font.render(text, True, color), (x, y))


def main():
    # Make sure that the choice selected by the user is valid
    print("Selecting character...")
    valid = False
    selected = None
    while not valid:
        try:
            selected = select_character()
            valid = n.send(selected.value)
        except TypeError:
            print("Please start the server")
            sys.exit()

    print("Creating player...")

    # How to wait for the start
    ready = False
    while not ready:
        show_ready()
        pygame.display.update()
        ready = n.send('start')

    print("Starting game...")
    board = Board(WIN)

    current_turn = n.send('whos_turn')
    player_positions = n.send('get_all_positions')

    # Some flags to keep track of if the game is quit early, if the player gets disqualified, and turn number
    disqualified = False
    run = True
    previous_turn = 0

    while run:
        # Ask whose turn it is
        turn_num = n.send('turn')
        cards = n.send(f'get_cards')
        notes = n.send(f'get_notes')

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
                n.send(f'update_position {player_positions[selected.value]}')
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
            disqualified = n.send(f'check_disqualified')

        # If the player has been disqualified, then add information to the screen to inform them
        if disqualified:
            draw_disqualification()

        # If the game has been won, then display the wining screen
        game_finished = n.send('game_finished')
        if game_finished:
            run = False
            draw_end_screen(selected)

        # If the game is quit early, then let the server that this player has quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Send a signal to the server that the game is being quit early
                n.send(f'early_quit')
                run = False

        # Update the window
        pygame.display.update()


main()
