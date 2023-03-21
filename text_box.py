import pygame as pg
pg.init()


class InputBox:
    def __init__(self, x, y, w, h, window):
        self.COLOR_INACTIVE = (0, 0, 0)
        self.COLOR_ACTIVE = (255, 255, 255)

        self.font_size = 16
        self.FONT = pg.font.Font('freesansbold.ttf', self.font_size)

        self.rect = pg.Rect(x, y, w, h)
        self.color = self.COLOR_INACTIVE

        self.limit = False
        self.full = False

        self.text = ['']
        self.labels = []
        self.active = False
        self.screen = window

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                # Start a new line
                if event.key == pg.K_RETURN:
                    self.text.append('')

                # Deleting
                elif event.key == pg.K_BACKSPACE:
                    if self.text:
                        self.text[len(self.text) - 1] = self.text[len(self.text) - 1][:-1]

                        if len(self.text) > 1 and self.text[len(self.text) - 1] == '':
                            self.text.pop()

                        if self.full:
                            self.full = False

                # Add text
                else:
                    self.update()
                    if not self.full:
                        self.text[len(self.text)-1] += event.unicode

                # Render the text
                self.labels = []
                for line in self.text:
                    self.labels.append(self.FONT.render(line, True, (0, 0, 0)))

    def update(self):
        # Start a new line if the text gets too long
        if self.labels and self.text[len(self.text) - 1] != '' and \
                self.labels[len(self.labels)-1].get_width() > self.rect.width - self.font_size - 5:
            if not self.limit:
                self.text.append('')
            else:
                self.full = True

        height = len(self.labels) * (self.font_size + 5)

        if height + self.font_size + 5 >= self.rect.height:
            if self.font_size > 10:
                self.font_size -= 1
            else:
                self.limit = True
        else:
            self.limit = False

    def draw(self):
        # Draw a background
        pg.draw.rect(self.screen, (192, 192, 192), (1000, 0, 300, 750))

        # Blit the text.
        for line in range(len(self.labels)):
            self.screen.blit(self.labels[line], (self.rect.x+5, self.rect.y+5 + (line * self.font_size) + (5 * line)))

        # Blit the rect.
        pg.draw.rect(self.screen, self.color, self.rect, 2)
