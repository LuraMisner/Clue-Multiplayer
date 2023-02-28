import constants
import pygame
import random
from board import Board
from characters import Characters
from network import Network


WIN = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Clue")
pygame.init()
card_map = {}


def draw_screen(board, cards, character, notes):
    board.draw_board()
    draw_cards(cards)
    draw_notes(character.value, notes)


def draw_notes(name, notes):
    header = pygame.font.SysFont('freesansbold.ttf', 32)
    title = pygame.font.SysFont('freesansbold.ttf', 24)
    font = pygame.font.SysFont('freesansbold.ttf', 20)

    WIN.blit(header.render(f"{name}'s notes", True, constants.BLACK), (675, 30))

    # Characters
    WIN.blit(title.render("It can't be these characters: ", True, constants.BLACK), (675, 70))
    for i, character in enumerate(notes[0]):
        x = 680 + (i//4 * 125)
        y = 95 + ((i % 4) * 20)
        WIN.blit(font.render(f"{character}", True, constants.BLACK), (x, y))

    # Weapons
    WIN.blit(title.render("It can't be these weapons: ", True, constants.BLACK), (675, 200))
    for i, weapon in enumerate(notes[1]):
        x = 680 + (i//4 * 125)
        y = 225 + ((i % 4) * 20)
        WIN.blit(font.render(f"{weapon}", True, constants.BLACK), (x, y))

    # Locations
    WIN.blit(title.render("It can't be these locations: ", True, constants.BLACK), (675, 325))
    for i, location in enumerate(notes[2]):
        x = 680 + (i//4 * 125)
        y = 350 + ((i % 4) * 20)
        WIN.blit(font.render(f"{location}", True, constants.BLACK), (x, y))


def draw_cards(cards):
    title = pygame.font.SysFont('freesansbold.ttf', 20)
    font = pygame.font.SysFont('freesansbold.ttf', 14)
    WIN.blit(title.render('Your cards ', True, constants.BLACK), (265, 635))

    for i, card in enumerate(cards):
        x = 10 + ((i % 6) * 100)
        y = 655 + (30 * (i // 6))

        rect = pygame.Rect(x, y, constants.CARD_SIZE_X, constants.CARD_SIZE_Y)
        pygame.draw.rect(WIN, constants.CARD, rect)
        card_value = card.get_value()
        card_map[card_value] = (x, y)

        WIN.blit(font.render(f'{card_value}', True, constants.BLACK),
                 (x + 2.5*(17 - len(card_value)), y + 5))


def show_ready(n):
    # Show how many players are ready
    WIN.fill(constants.BACKGROUND)
    num_ready = n.send('num_ready')
    font = pygame.font.SysFont('freesansbold.ttf', 56)
    WIN.blit(font.render(f'Waiting on other players...', True, (0, 0, 0)), (275, 200))
    WIN.blit(font.render(f'{num_ready[1]} out of {num_ready[0]} players ready', True, constants.BLACK), (275, 275))


def select_character(n) -> Characters:
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

        WIN.blit(header.render('Select a Character', True, constants.BLACK), (300, 200))

        mapping = {}
        # Character options
        for i, ch in enumerate(available_characters):
            x = 75 + i * 150
            y = 300
            mapping[ch] = (x, y)

            if ch == Characters.COLONEL_MUSTARD:
                color = constants.MUSTARD
            elif ch == Characters.MISS_SCARLET:
                color = constants.SCARLET
            elif ch == Characters.MR_PEACOCK:
                color = constants.PEACOCK
            elif ch == Characters.MRS_WHITE:
                color = constants.WHITE
            elif ch == Characters.PROFESSOR_PLUM:
                color = constants.PLUM
            else:
                # Reverend Green
                color = constants.GREEN

            rect = pygame.Rect(x, y, constants.CHARACTER_SELECTION_SIZE, constants.CHARACTER_SELECTION_SIZE)
            pygame.draw.rect(WIN, color, rect)

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


def whos_turn(n):
    who = n.send('whos_turn')
    font = pygame.font.SysFont('freesansbold.ttf', 24)
    WIN.blit(font.render(f"It's {who.get_character().value}'s turn", True, constants.BLACK), (700, 725))
    return who.get_character()


def handle_turn(our_location):
    moves = random.randint(2, 12)



def main():
    n = Network()
    print("Selecting character...")
    selected = select_character(n)
    print("Creating player...")
    n.send(selected.value)

    # How to wait for the start
    ready = False
    while not ready:
        show_ready(n)
        pygame.display.update()
        ready = n.send('start')

    print("Starting game...")
    board = Board(WIN)

    print("Getting cards...")
    cards = n.send(f'get_cards {selected.value}')

    print("Getting notes...")
    notes = n.send(f'get_notes {selected.value}')

    game_finished = False
    while not game_finished:
        draw_screen(board, cards, selected, notes)
        current_turn = whos_turn(n)

        # Handle our turn
        if current_turn == selected:
            handle_turn(n)

        pygame.display.update()
        game_finished = n.send('game_finished')


main()
