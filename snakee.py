import pygame
import random
import time

# import winsound

SIZE = 25
RES_X = 40 * SIZE
RES_Y = 25 * SIZE
fps = 200
speed = 0


pygame.init()

pygame.mixer.init()
pygame.mixer.music.load('fight.mp3')
pygame.mixer.music.play()
apple_get_sound = pygame.mixer.Sound("apple_sound.mp3")


surface = pygame.display.set_mode([RES_X, RES_Y])
clock = pygame.time.Clock()
img = pygame.image.load('fon.jpg').convert()
font_score = pygame.font.SysFont('Arial', 14, bold=False)

x = 4 * SIZE
y = 2 * SIZE
snake_direction = "right"
snake = [(x, y)]
snake_length = 6
score = snake_length
for i in range(1, snake_length):
    snake.append((snake[i - 1][0] - SIZE * 1, y))
# print(snake)

# generate 1st apple
apple_ok = False
while not apple_ok:
    apple_x = random.randint(0, RES_X // SIZE - 1) * SIZE
    apple_y = random.randint(0, RES_Y // SIZE - 1) * SIZE
    apple_ok = True
    for i in range(0, snake_length):
        if snake[i][0] == apple_x and snake[i][1] == apple_y:
            apple_ok = False
            print("apple_notOK")

# generate 1st teleport
teleport_ok = False
while not teleport_ok:
    teleport_x1 = random.randint(0, RES_X // SIZE - 1) * SIZE
    teleport_y1 = random.randint(0, RES_Y // SIZE - 1) * SIZE
    teleport_x2 = random.randint(0, RES_X // SIZE - 1) * SIZE
    teleport_y2 = random.randint(0, RES_Y // SIZE - 1) * SIZE
    teleport_ok = True
    for i in range(0, snake_length):
        if (snake[i][0] == teleport_x1 and snake[i][1] == teleport_y1) or (
                snake[i][0] == teleport_x2 and snake[i][1] == teleport_y2):
            teleport_ok = False
            print("teleport_notOK")

jj = 1
clock_ticker = 0
snake_dir_changed = 0
grad_inc = True
teleported = False
snake_dir_changed = 0
# score block
bestscore = 0
try:
    with open("score.txt", "r") as file:
        bestscore = int(file.readline())
        print(f"bestscore = {bestscore}")
except IOError:
    with open("score.txt", "w") as file:
        file.write("0")
# print(bestscore)


#queue for snake turns
turnqueue = [snake_direction]
zzt = []

game_start = 0




# time.sleep(1)
# main loop
while True:
    # find keypressed event
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
            if key == 82 and turnqueue[-1] != "down" and turnqueue[-1] != "up":
                snake_direction = "up"
                if len(turnqueue) == 1 and snake_dir_changed == 1:
                    turnqueue[0] = snake_direction
                else:
                    turnqueue.append(snake_direction)
                snake_dir_changed = 0
                # print("dir = 'up'")
                # break
            if key == 81 and turnqueue[-1] != "up" and turnqueue[-1] != "down":
                snake_direction = "down"
                if len(turnqueue) == 1 and snake_dir_changed == 1:
                    turnqueue[0] = snake_direction
                else:
                    turnqueue.append(snake_direction)
                snake_dir_changed = 0
                # break
            if key == 80 and turnqueue[-1] != "right" and turnqueue[-1] != "left":
                snake_direction = "left"
                if len(turnqueue) == 1 and snake_dir_changed == 1:
                    turnqueue[0] = snake_direction
                else:
                    turnqueue.append(snake_direction)
                snake_dir_changed = 0
                # break
            if key == 79 and turnqueue[-1] != "left" and turnqueue[-1] != "right":
                snake_direction = "right"
                if len(turnqueue) == 1 and snake_dir_changed == 1:
                    turnqueue[0] = snake_direction
                else:
                    turnqueue.append(snake_direction)
                snake_dir_changed = 0
                # break

    # move snake every 20 ticks
    if clock_ticker == 20:
        clock_ticker = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        snake_direction = turnqueue[0]
        if snake_direction == "up":
            y -= SIZE
        if snake_direction == "down":
            y += SIZE
        if snake_direction == "right":
            x += SIZE
        if snake_direction == "left":
            x -= SIZE
        snake_dir_changed = 1
        if turnqueue != zzt:
            zzt = turnqueue.copy()
            print(turnqueue)
        if len(turnqueue) > 1:
            for i in range(len(turnqueue) - 1):
                turnqueue[i] = turnqueue[i + 1]
            turnqueue.pop()

        if x >= RES_X:
            x = 0
        if x <= 0 - SIZE:
            x = RES_X // SIZE * SIZE - SIZE
        if y >= RES_Y:
            y = 0
        if y <= 0 - SIZE:
            y = RES_Y // SIZE * SIZE - SIZE

        # apple eat block
        if snake[0][0] == apple_x and snake[0][1] == apple_y:
            pygame.mixer.Sound.play(apple_get_sound)
            apple_ok = False
            while not apple_ok:
                apple_x = random.randint(0, RES_X // SIZE - 1) * SIZE
                apple_y = random.randint(0, RES_Y // SIZE - 1) * SIZE
                apple_ok = True
                for i in range(0, snake_length):
                    if snake[i][0] == apple_x and snake[i][1] == apple_y:
                        apple_ok = False
                        print("apple_notOK")
            for i in range(10):
                snake.append((snake[snake_length - 1][0], snake[snake_length - 1][1]))
                snake_length += 1
                score += 1
            # winsound.Beep(500, 10)

        # teleport block
        if not teleported:
            if snake[0][0] == teleport_x1 and snake[0][1] == teleport_y1:
                x = teleport_x2
                y = teleport_y2
                teleported = True
            if snake[0][0] == teleport_x2 and snake[0][1] == teleport_y2:
                x = teleport_x1
                y = teleport_y1
                teleported = True
            teleport_ok = False
            if teleported:
                while not teleport_ok:
                    teleport_x1 = random.randint(0, RES_X // SIZE - 1) * SIZE
                    teleport_y1 = random.randint(0, RES_Y // SIZE - 1) * SIZE
                    teleport_x2 = random.randint(0, RES_X // SIZE - 1) * SIZE
                    teleport_y2 = random.randint(0, RES_Y // SIZE - 1) * SIZE
                    teleport_ok = True
                    for i in range(0, snake_length):
                        if (snake[i][0] == teleport_x1 and snake[i][1] == teleport_y1) or (
                                snake[i][0] == teleport_x2 and snake[i][1] == teleport_y2):
                            teleport_ok = False
                            print("teleport_notOK")
        else:
            teleported = False

        # die block
        for i in range(snake_length):
            if x == snake[i][0] and y == snake[i][1]:
                if score > bestscore:
                    try:
                        with open("score.txt", "w") as file:
                            file.write(str(score))
                    except:
                        pass
                time.sleep(5)
                pygame.quit()
                exit()

        # move all parts of snake to new positions
        for i in range(snake_length - 1, 0, -1):
            snake[i] = (snake[i - 1][0], snake[i - 1][1])
        snake[0] = (x, y)


    # idk what is this
    surface.blit(img, (0, 0))
    render_score = font_score.render(f'Bestscore: {bestscore}. Your score: {score}', 1, pygame.Color('orange'))
    surface.blit(render_score, (5, 5))
    # pygame.draw.rect(surface, pygame.Color('green'), (x, y, 50, 50))

    # draw snake
    # draw snake head
    pygame.draw.rect(surface, pygame.Color(100, 250, 0), (snake[0][0], snake[0][1], SIZE, SIZE))
    # pygame.draw.circle(surface, pygame.Color(100, 250, 0, 0),
    # (snake[0][0] + SIZE // 2, snake[0][1] + SIZE // 2), SIZE // 2, width=1)
    # draw snake parts
    for i in range(1, snake_length):
        kt = int(i / snake_length * 5) + 3
        kt2 = kt - 2
        # print(kt)
        pygame.draw.rect(surface, pygame.Color(jj, jj, jj),
                         (snake[i][0] + kt2, snake[i][1] + kt2, SIZE - kt2 * 2, SIZE - kt2 * 2))
        pygame.draw.rect(surface, pygame.Color(int((i / snake_length) * 255), 255, 255 - int(i / snake_length * 255)),
                         (snake[i][0] + kt, snake[i][1] + kt, SIZE - 2 * kt, SIZE - 2 * kt))
    # pygame.draw.rect(surface, pygame.Color(int((i / snake_length) * 255), 255, 255 - int(i / snake_length * 255)),
    #      (snake[i][0], snake[i][1], SIZE, SIZE))

    # draw apple
    pygame.draw.circle(surface, pygame.Color(30, 255, 30), (apple_x + SIZE // 2, apple_y + SIZE // 2), SIZE // 3)
    # pygame.draw.circle(surface, pygame.Color(255, 255, 255), (apple_x + SIZE // 2, apple_y + SIZE // 2), SIZE // 2))

    # draw teleport
    pygame.draw.rect(surface, pygame.Color(200, jj, 150), (teleport_x1, teleport_y1, SIZE, SIZE), width=2)
    pygame.draw.rect(surface, pygame.Color(200, 255 - jj, 150), (teleport_x2, teleport_y2, SIZE, SIZE), width=2)

    pygame.display.flip()

    # color changer for teleport and snake
    if grad_inc:
        jj += 1
    else:
        jj -= 1

    if jj > 255:
        grad_inc = False
        jj = 255
    if jj < 1:
        grad_inc = True
        jj = 1

    # this is for moving snake every 20 ticks
    clock_ticker += 1

    clock.tick(fps + speed)
    if game_start == 0:
        game_start = 1
        time.sleep(1.7)
