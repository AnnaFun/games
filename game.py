import pygame_menu
import pygame
import math

import time

S_WIDTH = 600
S_HEIGHT = 600

game_over_happened = False


class Ball:
    def __init__(self, x, y, r, dx, dy, color):
        self.x = x
        self.y = y
        self.r = r
        self.dx = dx
        self.dy = dy
        self.color = color

    def move(self):
        if self.x - self.r <= 0 or self.x + self.r >= S_WIDTH:
            self.dx = -self.dx

        if self.y - self.r <= 0 or self.y + self.r >= S_WIDTH:
            self.dy = -self.dy

        self.x += self.dx
        self.y += self.dy

        if self.y >= (S_HEIGHT - self.r):
            global game_over_happened
            game_over_happened = True
            print("game_over_happened")

    def draw(self, sc):
        pygame.draw.circle(sc, self.color, (self.x, self.y), self.r)

    def check_collision(self, other_ball):
        l = math.sqrt((self.x - other_ball.x) ** 2 + (self.y - other_ball.y) ** 2)
        return l < self.r + other_ball.r

    def punch(self, other_ball):
        self.dx, other_ball.dx = other_ball.dx, self.dx


class Brick:
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, sc):
        pygame.draw.rect(sc, self.color, self.rect)


class Wall:
    def __init__(self, col, row, w, h):
        self.col = col
        self.row = row
        self.w = w
        self.h = h

        x_diff = (S_WIDTH - (col * w)) / (col - 1)

        self.bricks = []

        for i in range(col):
            for j in range(row):
                new_brick = Brick(i * (self.w + x_diff), j * (self.h + 10), self.w, self.h,
                                  (20, 78, 32))
                self.bricks.append(new_brick)

    def draw(self, sc):
        for brick in self.bricks:
            brick.draw(sc)

    def update_collision(self, ball):
        for brick in self.bricks:
            hits_brick_on_x = (ball.x > brick.x and ball.x < brick.x + brick.w)
            hits_brick_on_y = (brick.y + brick.h > ball.y - ball.r) and (brick.y < ball.y + ball.r)
            if hits_brick_on_x and hits_brick_on_y:
                self.bricks.remove(brick)
                ball.dy = -ball.dy


class Player:
    def __init__(self, w, color=(28, 129, 48)):
        self.w = w
        self.h = h = 15
        self.x = (S_WIDTH / 2) - (w / 2)
        self.y = S_HEIGHT - self.h - 10
        self.color = color
        self.speed = 8

    def draw(self, sc):
        rect = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(sc, self.color, rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < S_WIDTH:
            self.x += self.speed

    def update_collision(self, ball):
        ball_on_the_platform = (ball.x > self.x and ball.x < self.x + self.w)
        if (ball.y + ball.r > self.y) and (ball_on_the_platform):
            ball.dy = -ball.dy


def main():
    bg_color = (220, 220, 220)

    wall = Wall(6, 3, 80, 40)

    player = Player(180)

    ball = Ball(120, 300, 20, 5, 4, color=(222, 114, 1))

    is_ran = True
    while is_ran:
        screen.fill(bg_color)

        player.move()
        player.update_collision(ball)

        ball.move()

        wall.update_collision(ball)

        wall.draw(screen)
        ball.draw(screen)
        player.draw(screen)

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                is_ran = False

        if game_over_happened:
            is_ran = False

        pygame.display.update()

        time.sleep(1 / 90) #фпс


if __name__ == '__main__':
    while True:
        pygame.init()
        screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
        pygame.display.set_caption('Игра с мячиком')
        if game_over_happened:
            game_over_happened = False
            menu = pygame_menu.Menu(500, 500, 'Game over!')
            menu.add_button('Играть снова', main)
        else:
            menu = pygame_menu.Menu(300, 400, 'Привет!')
            menu.add_button('ИГРАТЬ', main)
        menu.mainloop(screen)