import pygame
import random

pygame.init()

# Sounds
BOUNCE_SOUND = pygame.mixer.Sound("bounce.wav")
LOOSE_SOUND = pygame.mixer.Sound("loose.wav")

WIN_WIDTH, WIN_HEIGHT = 1200, 600
WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Pong")

FPS = 30
SCALE = 20
WIDTH, HEIGHT = int(WIN_WIDTH / SCALE), int(WIN_HEIGHT / SCALE)

# Bat properties
BAT_WIDTH = 3

# Colors
BG = [55, 55, 55]
WHITE = [230, 230, 230]


class Score:
    def __init__(self, p):
        self.y = SCALE
        if p == 1:
            self.x = int(WIN_WIDTH / 2 - (SCALE*5))
        if p == 2:
            self.x = int(WIN_WIDTH / 2 + (SCALE*3))
        self. score = 0

    def Point(self):
        self.score += 1

    def Draw(self):
        text = pygame.font.SysFont('comicsans', 100)
        label = text.render(f"{self.score}", 1, WHITE)
        WINDOW.blit(label, (self.x, self.y))


class Ball:
    def __init__(self):
        global SCALE
        SCALE = SCALE
        self.radius = int(SCALE/2)
        self.angles = [0, 1, 2]
        self.y_speed = random.choice(self.angles)
        self.x_speed = 1

        self.x_speed = random.choice([self.x_speed, -self.x_speed])

        self.pos = [int(WIDTH/2), random.choice(range(self.radius, HEIGHT - self.radius))]

    def Bounce(self):
        if int(self.pos[1] * SCALE) <= self.radius*2 or int(self.pos[1] * SCALE) >= WIN_HEIGHT - self.radius*2:
            self.y_speed = -self.y_speed
            #BOUNCE_SOUND.play()

    def Hit_Bounce(self, bounce, ang):
        if bounce:
            self.x_speed = -self.x_speed
            self.y_speed = ang

    def Update(self):
        self.pos = [self.pos[0] + self.x_speed, self.pos[1] + self.y_speed]

    def Outside(self):
        if int(self.pos[0] * SCALE) <= self.radius * 2:
            LOOSE_SOUND.play()
            return 2
        elif int(self.pos[0] * SCALE) >= WIN_WIDTH - self.radius*2:
            LOOSE_SOUND.play()
            return 1
        else:
            return False

    def Draw(self):
        self.Bounce()
        self.Update()
        pygame.draw.circle(WINDOW, WHITE, (int(self.pos[0] * SCALE), int(self.pos[1] * SCALE)), int(self.radius))


class Bat:
    def __init__(self, x, y, up, down):
        global SCALE
        SCALE = SCALE

        self.x = x
        self.y = y

        self.up = up
        self.down = down

        self.height = 5
        self.gap = HEIGHT / 20

    def Move(self):
        keys = pygame.key.get_pressed()
        if keys[self.up] and self.y >= self.height / 2 + self.gap:  # up
            self.y -= 1
        if keys[self.down] and self.y <= HEIGHT - self.height / 2 - self.gap:  # down
            self.y += 1

    def Draw(self):
        self.Move()
        pygame.draw.rect(WINDOW, WHITE,
                         (int(self.x * SCALE), int((self.y - self.height / 2) * SCALE), int(SCALE),
                          int(SCALE * self.height)))

    def Hit(self, ball):
        x = ball.pos[0]
        y = ball.pos[1]
        angle = ball.y_speed
        radius = ball.radius
        bounce = False

        if self.x*SCALE + radius*2 == x * SCALE or self.x*SCALE - radius*2 == x * SCALE:
            if self.y == y:
                bounce = True
                angle = 0
            elif self.y - 1 == y:
                bounce = True
                angle = -1
            elif self.y - 2 == y:
                bounce = True
                angle = -2
            elif self.y + 1 == y:
                bounce = True
                angle = 1
            elif self.y + 2 == y:
                bounce = True
                angle = 2

            if bounce:
                BOUNCE_SOUND.play()

        ball.Hit_Bounce(bounce, angle)


def main():
    clock = pygame.time.Clock()
    global FPS, WHITE
    run = True

    L_Bat = Bat(1, int(HEIGHT / 2), pygame.K_w, pygame.K_s)
    R_Bat = Bat(int(WIDTH - BAT_WIDTH/2), int(HEIGHT / 2), pygame.K_UP, pygame.K_DOWN)
    ball = Ball()

    Scores = [Score(1), Score(2)]

    while run:
        clock.tick(FPS)

        WINDOW.fill(BG)
        L_Bat.Draw()
        R_Bat.Draw()
        Scores[0].Draw()
        Scores[1].Draw()
        ball.Draw()

        L_Bat.Hit(ball)
        R_Bat.Hit(ball)

        winner = ball.Outside()
        if winner:
            winner -= 1
            Scores[winner].Point()
            ball.__init__()

        pygame.draw.rect(WINDOW, WHITE, (int(WIN_WIDTH / 2), 0, 0, WIN_HEIGHT))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for score in Scores:
            if score.score >= 50:
                return True
    return False




if __name__ == "__main__":
    Play = True
    while Play:
        if not main():
            Play = False

