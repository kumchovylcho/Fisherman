import pygame
from boat import Boat
from fish import Fish

SIZE = (1600, 900)
pygame.init()
screen = pygame.display.set_mode(SIZE)

background = pygame.image.load("images/background.png")

boat = Boat()
left_picture_boat, right_picture_boat = boat.load_boat()
fish = Fish(800, 500)
left_picture_fish, right_picture_fish = fish.load_pictures()

running = True
boat_look_direction = left_picture_boat
fish_look_direction = left_picture_fish if fish.x_pos <= SIZE[0] // 2 else right_picture_fish
while running:
    pygame.time.Clock().tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.key.get_pressed()[pygame.K_a]:
        boat.move_left()
        boat_look_direction = left_picture_boat
    elif pygame.key.get_pressed()[pygame.K_d]:
        boat.move_right()
        boat_look_direction = right_picture_boat

    seconds = pygame.time.get_ticks() // 1000
    if fish_look_direction == left_picture_fish:
        fish.swim_left(seconds)
        if fish.check_left_wall():
            fish_look_direction = right_picture_fish
    elif fish_look_direction == right_picture_fish:
        fish.swim_right(seconds)
        screen_width = SIZE[0]
        if fish.check_right_wall(screen_width):
            fish_look_direction = left_picture_fish

    screen.blit(background, (0, 0))
    screen.blit(boat_look_direction, (boat.x, boat.y))
    screen.blit(fish_look_direction, (fish.x_pos, fish.y_pos))
    pygame.display.update()
