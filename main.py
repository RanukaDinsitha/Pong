import pygame
import sys
import random
import math
import threading, time
from snap import snap

pygame.init()
pygame.mixer.init()
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=2048) 

# ------------------ Window Setup ------------------
ICON = pygame.image.load("./assets/icon.png")
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")
pygame.display.set_icon(ICON)
dev_test = True
snap_mode = False

FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ------------------ Game Variables ------------------
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

if dev_test == False:
    try:
        SCORE_FONT = pygame.font.Font("./assets/number.ttf", 50)
        HIT_SOUND = pygame.mixer.Sound("./assets/paddle_hit.wav")
        END_CHEERING_YAY = pygame.mixer.Sound("./assets/crowd_cheering.wav")
    except pygame.error as e:
        print(f"Critical error, please look if the assets folder is in the directory you placed this app?: {e}")
        sys.exit(1)
else: 
    SCORE_FONT = pygame.font.Font("./assets/number.ttf", 50)
    HIT_SOUND = pygame.mixer.Sound("./assets/paddle_hit.wav")
    END_CHEERING_YAY = pygame.mixer.Sound("./assets/crowd_cheering.wav")

POINT_EXTRA_AUDIO = pygame.mixer.Sound("./assets/score_audio.mp3")

if dev_test:
    WINNING_SCORE = 5
else:
    WINNING_SCORE = 35

# ------------------ Paddle Class ------------------


class Paddle:
    COLOR = WHITE
    VEL = 6

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(
            win,
            self.COLOR,
            (self.x,
             self.y,
             self.width,
             self.height))

    def move(self, up=True):
        if up and self.y > 0:
            self.y -= self.VEL
        elif not up and self.y + self.height < HEIGHT:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

# ------------------ Ball Class ------------------


class Ball:
    COLOR = WHITE
    MAX_VEL = 5

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.x_vel *= -1
        self.y_vel = 0

# ------------------ Drawing Function ------------------


def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)
    left_score_text = SCORE_FONT.render(f"{left_score}", True, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", True, WHITE)
    win.blit(
        left_score_text,
        (WIDTH //
         4 -
         left_score_text.get_width() //
         2,
         20))
    win.blit(right_score_text, (WIDTH * 3 // 4 -
             right_score_text.get_width() // 2, 20))

    for paddle in paddles:
        paddle.draw(win)

    ball.draw(win)

    for i in range(10, HEIGHT, HEIGHT // 20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH // 2 - 5, i, 10, HEIGHT // 20))

    pygame.display.update()

# ------------------ Collision Function ------------------

def handle_collision(ball, left_paddle, right_paddle):
    # Bounce on top/bottom walls (make it bouncier)
    if ball.y + ball.radius >= HEIGHT or ball.y - ball.radius <= 0:
        ball.y_vel *= -1.05  # reverse + small boost

        # Cap vertical speed
        if abs(ball.y_vel) > ball.MAX_VEL:
            ball.y_vel = ball.MAX_VEL * (1 if ball.y_vel > 0 else -1)

    # Left paddle
    if ball.x_vel < 0:
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1.1  # more bounce off paddle
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_y = ball.y - middle_y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                ball.y_vel = difference_y / reduction_factor
                ball.y_vel *= 1.25  # more curve/spin effect

                # Speed cap
                ball.x_vel = max(min(ball.x_vel, ball.MAX_VEL), -ball.MAX_VEL)
                ball.y_vel = max(min(ball.y_vel, ball.MAX_VEL), -ball.MAX_VEL)

                HIT_SOUND.play()
    # Right paddle
    else:
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1.1 * 2
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_y = ball.y - middle_y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                ball.y_vel = difference_y / reduction_factor
                ball.y_vel *= 1.25

                ball.x_vel = max(min(ball.x_vel, ball.MAX_VEL), -ball.MAX_VEL)
                ball.y_vel = max(min(ball.y_vel, ball.MAX_VEL), -ball.MAX_VEL)

                HIT_SOUND.play()

# ------------------ Paddle Controls ------------------


def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + \
            left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + \
            right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)

 # ------------------ Main Function ------------------
def main():
    clock = pygame.time.Clock()
    run = True

    left_paddle = Paddle(
        10,
        HEIGHT //
        2 -
        PADDLE_HEIGHT //
        2,
        PADDLE_WIDTH,
        PADDLE_HEIGHT)
    right_paddle = Paddle(
        WIDTH - 10 - PADDLE_WIDTH,
        HEIGHT // 2 - PADDLE_HEIGHT // 2,
        PADDLE_WIDTH,
        PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    left_score = 0
    right_score = 0

    left_oob = pygame.Rect(-50, 0, 50, HEIGHT)
    right_oob = pygame.Rect(WIDTH, 0, 50, HEIGHT)

    while run:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        # Out-of-bounds scoring
        ball_rect = pygame.Rect(
            ball.x - ball.radius,
            ball.y - ball.radius,
            ball.radius * 2,
            ball.radius * 2)
        if ball_rect.colliderect(left_oob):
            right_score += 1
            POINT_EXTRA_AUDIO.play()
            ball.reset()
        elif ball_rect.colliderect(right_oob):
            left_score += 1
            POINT_EXTRA_AUDIO.play()
            ball.reset()

        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        if left_score >= WINNING_SCORE:
            start_celebration("left")
        elif right_score >= WINNING_SCORE:
            start_celebration("right")
            
        snap()

            

    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
