import pygame
from random import randrange

pygame.init()
WINDOW = 1000

time, time_step = 0, 110
screen = pygame.display.set_mode((WINDOW, WINDOW)) #sets window size
clock = pygame.time.Clock() #frame rate

#CREATING THE MAP
TILE_SIZE = 50 # sets the tile size
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE) # sets the center of each tiles, (start, stop, step) for randrange
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)] # grabs one tile center

#CREATING THE SNAKE
snake = pygame.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2]) # creates the snake head
snake.center = get_random_position() # put the snake in a random position

snake_dir = (0, 0)

length = 1
segments = [snake.copy()]

food = snake.copy()
food.center = get_random_position()

dirs = {pygame.K_w: 1, pygame.K_s: 1, pygame.K_a: 1, pygame.K_d: 1}

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and dirs[pygame.K_w]:
                snake_dir = (0, -TILE_SIZE) #up
                dirs = {pygame.K_w: 1, pygame.K_s: 0, pygame.K_a: 1, pygame.K_d: 1}

            if event.key == pygame.K_s and dirs[pygame.K_s]:
                snake_dir = (0, TILE_SIZE) #down
                dirs = {pygame.K_w: 0, pygame.K_s: 1, pygame.K_a: 1, pygame.K_d: 1}

            if event.key == pygame.K_a  and dirs[pygame.K_a]:
                snake_dir = (-TILE_SIZE, 0) #left
                dirs = {pygame.K_w: 1, pygame.K_s: 1, pygame.K_a: 1, pygame.K_d: 0}

            if event.key == pygame.K_d and dirs[pygame.K_d]:
                snake_dir = (TILE_SIZE, 0) #right
                dirs = {pygame.K_w: 1, pygame.K_s: 1, pygame.K_a: 0, pygame.K_d: 1}

     # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    # check borders and self eating
    food_in_tail = pygame.Rect.collidelist(food, segments[:-1]) != -1
    if food_in_tail:
        food.center = get_random_position()
        
    self_eating = pygame.Rect.collidelist(snake, segments[:-1]) != -1
    if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW or self_eating:
        snake.center, food.center = get_random_position(), get_random_position()
        length, snake_dir =  1, (0,0)
        segments = [snake.copy()]
    # check food

    if snake.center == food.center:
        food.center = get_random_position()
        length += 1

    # draw food
    pygame.draw.rect(screen, 'red', food)
    # drawing the snake 
    [pygame.draw.rect(screen, 'green', segment) for segment in segments] #enables a loop so the snake is drawned by length
    # move snake
    time_now = pygame.time.get_ticks()
    if time_now - time > time_step: #controls the time 
        time = time_now
        snake.move_ip(snake_dir)
        segments.append(snake.copy()) #records previous step
        segments = segments[-length:] # : sets the range of the size. length = 1.. turning it into -1 towards whatever is at the end of the list


    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()