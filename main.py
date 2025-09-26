import pygame
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
FPS = int(30)
# Note, in the original it was 60, if having problems switch to 60 :)

# Define the colors Black & White:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define the Paddle's Width, and the Paddle's Height!
PADDLE_WIDTH, PADDLE_HEIGHT, = int(20), int(100)

# Start the class for our/AI's Paddle:
class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rectangle(win, self.COLOR, ())

# The drawing function. *pretends to be an artist*:
def draw(win):
    win.fill(BLACK)
    pygame.display.update()


# Define the Main function.
def main():
    clock = pygame.time.Clock()
    run = True

    # Let's Python do some Math to get the Paddles to worth. *calculator button presses*
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

    while run:
        clock.tick(FPS)
        draw(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Asking the user if they want to quit.
                ask_quit = input("Are you sure you want to quit? (yes/no): \n").strip().lower()
                print(" ")
                if ask_quit == "yes":
                    print("Okay, thank you for playing! If you want to play again, just open the game file!")
                    sleep(0.75)
                    run = False
                elif ask_quit == "no":
                    print("No problem, continuing game!")
                    sleep(0.75)
                else:
                    print("Take that as a Yes. If you want to play again, just open the game file!")
                    sleep(0.75)
                    run = False
                break

    # Quit. :(
    pygame.quit()
            
if __name__ == '__main__':
    main()