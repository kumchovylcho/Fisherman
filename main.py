import pygame
from boat import Boat
from fish import Fish
from fishing_line import FishLine

SIZE = (1600, 900)
pygame.init()
screen = pygame.display.set_mode(SIZE)

background = pygame.image.load("images/background.png")

boat = Boat()
left_picture_boat, right_picture_boat = boat.load_boat()
fish = Fish(800, 500)
left_picture_fish, right_picture_fish = fish.load_pictures()
fisherman_line = FishLine()

boat_look_direction = left_picture_boat
fish_look_direction = left_picture_fish if fish.x_pos <= SIZE[0] // 2 else right_picture_fish

is_hook_moving = False
running = True
while running:
    pygame.time.Clock().tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                is_hook_moving = True

    seconds = pygame.time.get_ticks() // 1000
    if pygame.key.get_pressed()[pygame.K_a] and not is_hook_moving:
        boat.move_left(seconds)
        boat_look_direction = left_picture_boat
    elif pygame.key.get_pressed()[pygame.K_d] and not is_hook_moving:
        boat.move_right(seconds)
        boat_look_direction = right_picture_boat

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
    pygame.draw.line(screen, (255, 0, 0), fisherman_line.start_point, fisherman_line.end_point, 5)
    screen.blit(fish_look_direction, (fish.x_pos, fish.y_pos))
    screen.blit(fisherman_line.picture, (500, 500))
    pygame.display.update()
