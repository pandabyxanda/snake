"""
Snake game. Using OOP, type hints, comments.
Made using PyGame module.
Features: 1) teleport 2) color changing method 3) ...
"""

import pygame
import random
import time

# 123

class Snake:
    """Class for controlling full snake"""

    def __init__(self, game):
        self.game = game
        self.SIZE = 25
        self.x = 4 * self.SIZE
        self.y = 2 * self.SIZE
        self.direction = "right"
        # self.snake_prev_direction = self.snake_direction
        self.snake = [(self.x, self.y)]
        self.length = 6

        for i in range(1, self.length):
            self.snake.append((self.snake[i - 1][0] - self.SIZE * 1, self.y))

        self.snake_dir_changed = 0
        self.teleported = False

        self.grad_inc = True
        self.color = 0

        self.turnqueue = [self.direction]
        self.temp_turnqueue = []

        # self.game_start = 0

    def change_head_coord(self, keys):
        """Snake move"""
        self.direction = keys.turnqueue[0]
        # print(self.turnqueue)
        if self.direction == "up":
            self.y -= self.SIZE
        if self.direction == "down":
            self.y += self.SIZE
        if self.direction == "right":
            self.x += self.SIZE
        if self.direction == "left":
            self.x -= self.SIZE

        self.snake_dir_changed = 1
        # if keys.turnqueue != self.temp_turnqueue:
        #     self.temp_turnqueue = keys.turnqueue.copy()
        #     print(keys.turnqueue)
        if len(keys.turnqueue) > 1:
            for i in range(len(keys.turnqueue) - 1):
                keys.turnqueue[i] = keys.turnqueue[i + 1]
            keys.turnqueue.pop()

    def check_out_of_field(self):
        if self.x >= self.game.RES_X:
            self.x = 0
        if self.x <= 0 - self.game.SIZE:
            self.x = self.game.RES_X // self.game.SIZE * self.game.SIZE - self.game.SIZE
        if self.y >= self.game.RES_Y:
            self.y = 0
        if self.y <= 0 - self.game.SIZE:
            self.y = self.game.RES_Y // self.game.SIZE * self.game.SIZE - self.game.SIZE

    def change_body_pos(self):
        """move all parts of snake to positions of previous part closer to head"""
        for i in range(self.length - 1, 0, -1):
            self.snake[i] = (self.snake[i - 1][0], self.snake[i - 1][1])
        self.snake[0] = (self.x, self.y)
        self.check_die(score)

    def draw(self):

        # draw head
        pygame.draw.rect(game.surface, pygame.Color(100, 250, 0),
                         (self.snake[0][0], self.snake[0][1], self.SIZE, self.SIZE))

        if self.grad_inc:
            self.color += 1
        else:
            self.color -= 1

        if self.color > 255:
            self.grad_inc = False
            self.color = 255
        if self.color < 1:
            self.grad_inc = True
            self.color = 1

        # draw body
        for i in range(1, self.length):
            kt = int(i / self.length * 5) + 3
            kt2 = kt - 2
            # print(kt)
            pygame.draw.rect(self.game.surface, pygame.Color(self.color, self.color, self.color),
                             (self.snake[i][0] + kt2, self.snake[i][1] + kt2, self.SIZE - kt2 * 2, self.SIZE - kt2 * 2))
            pygame.draw.rect(self.game.surface,
                             pygame.Color(int((i / self.length) * 255), 255, 255 - int(i / self.length * 255)),
                             (self.snake[i][0] + kt, self.snake[i][1] + kt, self.SIZE - 2 * kt, self.SIZE - 2 * kt))

    def check_die(self, score):
        """Check if coords of head equal to coords of body pieces"""

        for i in range(1, self.length):
            if self.x == self.snake[i][0] and self.y == self.snake[i][1]:
                if score.score > score.bestscore:
                    try:
                        with open("score.txt", "w") as file:
                            file.write(str(score.score))
                    except:
                        pass

                # End of game
                self.draw()
                render_die_msg = game.die_score.render(f'You die...', 1, pygame.Color('red'))
                game.surface.blit(render_die_msg, (200, 200))
                pygame.display.flip()
                time.sleep(3)
                pygame.quit()
                exit()


class Game:
    """Class for window, music, fonts, speed of snake and speed of color changing"""

    def __init__(self):
        self.SIZE = 25
        self.RES_X = 40 * self.SIZE
        self.RES_Y = 25 * self.SIZE
        self.fps = 200
        self.speed = 0

    def init(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('fight.mp3')
        pygame.mixer.music.play()

        self.surface = pygame.display.set_mode([self.RES_X, self.RES_Y])
        self.clock = pygame.time.Clock()
        self.img = pygame.image.load('fon.jpg').convert()
        self.font_score = pygame.font.SysFont('Arial', 14, bold=False)
        self.die_score = pygame.font.SysFont('Arial', 80, bold=False)
        self.clock_ticker = 0
        print("game init OK")


class Score:
    """Class for reading, writing, drawing score"""

    def __init__(self, game, snake):
        self.game = game
        self.score = snake.length
        self.bestscore = 0
        try:
            with open("score.txt", "r") as file:
                self.bestscore = int(file.readline())
                print(f"bestscore = {self.bestscore}")
        except IOError:
            with open("score.txt", "w") as file:
                file.write("0")

    def draw_score(self):
        render_score = self.game.font_score.render(f'Bestscore: {self.bestscore}. Your score: {self.score}', 1,
                                                   pygame.Color('orange'))
        self.game.surface.blit(render_score, (5, 5))


class Apple:
    __num_of_apples = 0

    def __new__(cls, *args, **kwargs):
        cls.__num_of_apples += 1
        return super().__new__(cls)

    def __init__(self, game, snake, score):
        self.ok = False
        self.game = game
        self.snake = snake
        self.sound = pygame.mixer.Sound("apple_sound.mp3")
        self.score = score
        self.x = None
        self.y = None
        self.create_new()
        print(f"{self.__num_of_apples} apple init OK")

    def create_new(self):
        self.ok = False
        while not self.ok:
            self.x = random.randint(0, self.game.RES_X // self.game.SIZE - 1) * self.game.SIZE
            self.y = random.randint(0, self.game.RES_Y // self.game.SIZE - 1) * self.game.SIZE
            self.ok = True
            for i in range(0, self.snake.length):
                if self.snake.snake[i][0] == self.x and self.snake.snake[i][1] == self.y:
                    self.ok = False
                    print("apple_notOK")

    def draw(self):
        pygame.draw.circle(self.game.surface, pygame.Color(30, 255, 30),
                           (self.x + self.game.SIZE // 2, self.y + self.game.SIZE // 2), self.game.SIZE // 3)

    def check_eaten(self):
        # apple eat block
        if self.snake.snake[0][0] == self.x and self.snake.snake[0][1] == self.y:
            pygame.mixer.Sound.play(self.sound)

            self.create_new()

            for i in range(10):
                self.snake.snake.append(
                    (self.snake.snake[self.snake.length - 1][0], self.snake.snake[self.snake.length - 1][1]))
                self.snake.length += 1
                self.score.score += 1
            # winsound.Beep(500, 10)


class Teleport:
    def __init__(self, game: Game, snake: Snake, score: Score) -> object:
        self.game = game
        self.snake = snake
        self.score = score
        self.create_new()
        print("teleport init OK")

    def create_new(self) -> object:
        self.ok = False
        while not self.ok:

            self.x1 = random.randint(0, self.game.RES_X // self.game.SIZE - 1) * self.game.SIZE
            self.y1 = random.randint(0, self.game.RES_Y // self.game.SIZE - 1) * self.game.SIZE
            self.x2 = random.randint(0, self.game.RES_X // self.game.SIZE - 1) * self.game.SIZE
            self.y2 = random.randint(0, self.game.RES_Y // self.game.SIZE - 1) * self.game.SIZE
            self.ok = True
            for i in range(0, self.snake.length):
                if (self.snake.snake[i][0] == self.x1 and self.snake.snake[i][1] == self.y1) or (
                        self.snake.snake[i][0] == self.x2 and self.snake.snake[i][1] == self.y2):
                    self.ok = False
                    print("teleport_notOK")

    def check_teleport_reached(self):
        # teleport block
        if not self.snake.teleported:
            if self.snake.snake[0][0] == self.x1 and self.snake.snake[0][1] == self.y1:
                self.snake.x = self.x2
                self.snake.y = self.y2
                self.snake.teleported = True
            if self.snake.snake[0][0] == self.x2 and self.snake.snake[0][1] == self.y2:
                self.snake.x = self.x1
                self.snake.y = self.y1
                self.snake.teleported = True
            if self.snake.teleported:
                self.create_new()
                # self.snake.snake[0] = x, y

        else:
            self.snake.teleported = False

    def draw(self):
        # draw teleport
        pygame.draw.rect(self.game.surface, pygame.Color(200, self.snake.color, 150),
                         (self.x1, self.y1, self.game.SIZE, self.game.SIZE), width=2)
        pygame.draw.rect(self.game.surface, pygame.Color(200, 255 - self.snake.color, 150),
                         (self.x2, self.y2, self.game.SIZE, self.game.SIZE), width=2)


class Keys:
    def __init__(self, snake: Snake):
        self.turnqueue = [snake.direction]
        self.snake = snake

    def get_keys_queue(self):
        """This helps to remember all keys pressed one after another in own variable"""

        def queue_change():
            if len(self.turnqueue) == 1 and self.snake.snake_dir_changed == 1:
                self.turnqueue[0] = self.snake.direction
            else:
                self.turnqueue.append(self.snake.direction)
            self.snake.snake_dir_changed = 0

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # print(" ")
                # print(event)
                # print(event.scancode)
                # print(type(event.scancode))
                key = event.scancode
                if key == 41:
                    pygame.quit()

                # after last turn if queue is empty new direction is 1st in queue
                if key == 82 and self.turnqueue[-1] != "down" and self.turnqueue[-1] != "up":
                    self.snake.direction = "up"
                    queue_change()
                    # print("dir = 'up'")
                    # break
                if key == 81 and self.turnqueue[-1] != "up" and self.turnqueue[-1] != "down":
                    self.snake.direction = "down"
                    queue_change()
                    # break
                if key == 80 and self.turnqueue[-1] != "right" and self.turnqueue[-1] != "left":
                    self.snake.direction = "left"
                    queue_change()
                    # break
                if key == 79 and self.turnqueue[-1] != "left" and self.turnqueue[-1] != "right":
                    self.snake.direction = "right"
                    queue_change()
                    # break


# main code
game = Game()
game.init()
snake = Snake(game)
keys = Keys(snake)
score = Score(game, snake)
apple = Apple(game, snake, score)
apple1 = Apple(game, snake, score)
teleport = Teleport(game, snake, score)

# main loop
while True:
    keys.get_keys_queue()

    # speed of color changing is faster then the snake moving
    if game.clock_ticker == 20:
        game.clock_ticker = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        snake.change_head_coord(keys)
        apple.check_eaten()
        apple1.check_eaten()

        snake.check_out_of_field()
        teleport.check_teleport_reached()

        snake.change_body_pos()

    game.surface.blit(game.img, (0, 0))
    apple.draw()
    apple1.draw()
    teleport.draw()
    score.draw_score()
    snake.draw()

    pygame.display.flip()

    game.clock_ticker += 1
    game.clock.tick(game.fps + game.speed)
