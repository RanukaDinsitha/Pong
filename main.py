import pygame
import sys
from time import sleep

# Starting up Pygame to use for the Project!
pygame.init()

# Define the Width and the Height. Setup Window, and Set Caption & Set the Icon.
ICON = pygame.image.load("./assets/icon.png")
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")
pygame.display.set_icon(ICON)

# Sets the frames:
FPS = 60  # smoother
# Define the colors Black & White:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define the Paddle's Width, and the Paddle's Height!
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = int(7)

# Start the class for our/AI's Paddle:
class Paddle:
    COLOR = WHITE  # Paddles are White!
    VEL = 6

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    # Drawing function. *sighs in artist*    
    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    # Defines the Moving function for the Paddles.
    def move(self, up=True):
        if up and self.y > 0:
            self.y -= self.VEL
        elif not up and self.y + self.height < HEIGHT:
            self.y += self.VEL

class Ball:
    MAX_VEL = int(5)

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y                                                                                                                                                                                                              
        self.radius = radius
        self.x_vel = MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

# Helper function to draw a “key style” button
def draw_button(win, rect, text, active=False):
    font = pygame.font.SysFont("Arial", 28, bold=True)
    color = (180, 180, 180) if not active else (200, 200, 255)
    pygame.draw.rect(win, color, rect, border_radius=8)
    pygame.draw.rect(win, WHITE, rect, 2, border_radius=8)
    label = font.render(text, True, BLACK)
    win.blit(label, (rect.x + rect.width//2 - label.get_width()//2,
                     rect.y + rect.height//2 - label.get_height()//2))

# The drawing function. *pretends to be an artist*:
def draw(win, paddles, show_quit=False, buttons=None, farewell_text=False):
    win.fill(BLACK)
    
    # Draw the Paddles! :)
    for paddle in paddles:
        paddle.draw(win)

    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue

        ball.draw(win)
        pygame.draw.rect(win, WHITE, (WIDTH//2 - int(5), i, 10, HEIGHT//20))

    # Draw quit popup if needed.
    if show_quit:
        font = pygame.font.SysFont("Arial", 30)
        text1 = font.render("Are you sure you want to quit?", True, WHITE)
        text2 = font.render("Press button for Yes or No", True, WHITE)

        # Draw a rectangle behind text (like a popup box)!
        popup_width, popup_height = 420, 180
        popup_x = WIDTH // 2 - popup_width // 2
        popup_y = HEIGHT // 2 - popup_height // 2
        pygame.draw.rect(win, (50, 50, 50), (popup_x, popup_y, popup_width, popup_height))
        pygame.draw.rect(win, WHITE, (popup_x, popup_y, popup_width, popup_height), 2)

        # Draw the text
        win.blit(text1, (WIDTH // 2 - text1.get_width() // 2, popup_y + 20))
        win.blit(text2, (WIDTH // 2 - text2.get_width() // 2, popup_y + 60))

        if buttons:
            for rect, label in buttons:
                draw_button(win, rect, label)

    # Show farewell popup if quitting. *displays message*
    if farewell_text:
        font = pygame.font.SysFont("Arial", 26)
        text1 = font.render("Okay, thank you for playing!", True, WHITE)
        text2 = font.render("If you want to play again,", True, WHITE)
        text3 = font.render("just open the game file!", True, WHITE)

        # Draw a popup box
        popup_width, popup_height = 420, 180
        popup_x = WIDTH // 2 - popup_width // 2
        popup_y = HEIGHT // 2 - popup_height // 2
        pygame.draw.rect(win, (50, 50, 50), (popup_x, popup_y, popup_width, popup_height))
        pygame.draw.rect(win, WHITE, (popup_x, popup_y, popup_width, popup_height), 2)

        # Center text neatly inside box
        win.blit(text1, (WIDTH // 2 - text1.get_width() // 2, popup_y + 20))
        win.blit(text2, (WIDTH // 2 - text2.get_width() // 2, popup_y + 70))
        win.blit(text3, (WIDTH // 2 - text3.get_width() // 2, popup_y + 110))

    pygame.display.update()

# Handles the paddle controls! :D
def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)

# Define the Main function.
def main():
    clock = pygame.time.Clock()
    run = True
    confirming_quit = False
    farewell_mode = False
    farewell_start = 0

    # Let's Python do some Math to get the Paddles to work. *calculator button presses*
    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    # The Yes and No buttons. (styled as keys) :)
    yes_button = pygame.Rect(WIDTH//2 - 120, HEIGHT//2 + 80, 80, 40)
    no_button = pygame.Rect(WIDTH//2 + 40, HEIGHT//2 + 80, 80, 40)
    buttons = [(yes_button, "Y"), (no_button, "N")]

    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confirming_quit = True  # Show popup instead of quitting!
            if event.type == pygame.MOUSEBUTTONDOWN and confirming_quit and not farewell_mode:
                if yes_button.collidepoint(event.pos):
                    farewell_mode = True
                    farewell_start = pygame.time.get_ticks()
                elif no_button.collidepoint(event.pos):
                    confirming_quit = False

        if farewell_mode:
            now = pygame.time.get_ticks()
            if now - farewell_start >= 2000:
                run = False
            draw(WIN, [left_paddle, right_paddle], farewell_text=True)
        else:
            keys = pygame.key.get_pressed()
            if not confirming_quit:  # Stops, the paddle when it is open.
                handle_paddle_movement(keys, left_paddle, right_paddle)
            draw(WIN, [left_paddle, right_paddle], show_quit=confirming_quit, buttons=buttons)

    # Quit. :(
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
