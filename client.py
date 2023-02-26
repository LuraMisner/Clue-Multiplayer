import constants
import pygame
from board import Board
from characters import Characters
from network import Network


WIN = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Clue")
pygame.init()


def show_ready(n):
    # Show how many players are ready
    WIN.fill(constants.BACKGROUND)
    num_ready = n.send('num_ready')
    font = pygame.font.SysFont(None, 56)
    WIN.blit(font.render(f'Waiting on other players...', True, (0, 0, 0)), (275, 200))
    WIN.blit(font.render(f'{num_ready[1]} out of {num_ready[0]} players ready', True, (0, 0, 0)), (275, 275))


def select_character(n) -> Characters:
    selection_made = False
    choice = None

    while not selection_made:
        available_characters = n.send('character_selection')
        WIN.fill(constants.BACKGROUND)

        # How many players ready
        num_ready = n.send('num_ready')
        font1 = pygame.font.SysFont(None, 26)
        WIN.blit(font1.render(f'{num_ready[1]} out of {num_ready[0]} players ready', True, (0, 0, 0)), (50, 50))

        # Title
        header = pygame.font.SysFont(None, 60)
        font = pygame.font.SysFont(None, 32)

        WIN.blit(header.render('Select a Character', True, (0, 0, 0)), (300, 200))

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

        # Selection update
        WIN.blit(font.render('Character Selected: ', True, (0, 0, 0)), (300, 500))

        if choice:
            # If a choice has been made, add a confirmation button to create the player
            WIN.blit(font.render(choice.value, True, (0, 0, 0)), (550, 500))

            # Button to confirm selection (will confirm the selection made if choice != None
            rect = pygame.Rect(425, 600, 125, 65)
            pygame.draw.rect(WIN, (0, 0, 0), rect)
            rect = pygame.Rect(427, 602, 121, 61)
            pygame.draw.rect(WIN, (0, 255, 0), rect)

            WIN.blit(font.render('Confirm', True, (0, 0, 0)), (442, 622))

            # Listen for clicks
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()

                    # Clicking confirmed
                    x, y = pos
                    if 425 <= x <= 425 + 125 and 600 <= y <= 600 + 65:
                        selection_made = True

        pygame.display.update()

    return choice


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

    print("Loading board...")
    board.draw_board()

    game_finished = False
    while not game_finished:
        pygame.display.update()
        game_finished = n.send('game_finished')


main()
