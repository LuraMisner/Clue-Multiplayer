import pygame
from network import Network
from characters import Characters
from player import Player

pygame.init()
WIDTH = 1000
HEIGHT = 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")


def select_character(n) -> Characters:
    selection_made = False
    choice = None

    pygame.init()
    SQUARE_SIZE = 100

    # Colors
    WHITE = (255, 255, 255)
    MUSTARD = (189, 138, 11)
    PLUM = (89, 6, 138)
    GREEN = (9, 112, 30)
    SCARLET = (255, 3, 7)
    PEACOCK = (20, 41, 156)

    while not selection_made:
        available_characters = n.send('character_selection')
        WIN.fill((192, 192, 192))

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
                color = MUSTARD
            elif ch == Characters.MISS_SCARLET:
                color = SCARLET
            elif ch == Characters.MR_PEACOCK:
                color = PEACOCK
            elif ch == Characters.MRS_WHITE:
                color = WHITE
            elif ch == Characters.PROFESSOR_PLUM:
                color = PLUM
            else:
                # Reverend Green
                color = GREEN

            rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(WIN, color, rect)

        # Listen for clicks
        ev = pygame.event.get()
        for event in ev:

            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                # Find out if the click maps to a character
                for key in mapping.keys():
                    x, y = pos
                    x2, y2 = mapping[key]

                    if x2 < x < x2 + SQUARE_SIZE and y2 < y < y2 + SQUARE_SIZE:
                        choice = key

        # Selection update
        WIN.blit(font.render('Character Selected: ', True, (0, 0, 0)), (300, 500))

        if choice:
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

                # handle MOUSEBUTTONUP
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
    selected = select_character(n)
    n.send(selected.value)

main()
