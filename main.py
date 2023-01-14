import pygame
from boat import Boat
from fish import Fish
from fishing_line import FishLine
from hook import Hook
from info_json import *

SIZE = (1600, 900)
pygame.init()
screen = pygame.display.set_mode(SIZE)

background = pygame.image.load("images/background.png")

boat = Boat()
fish = Fish(800, 500)
fisherman_line = FishLine(boat)
hook = Hook(boat)

left_picture_boat, right_picture_boat = boat.load_boat()
left_picture_fish, right_picture_fish = fish.load_pictures()

boat_look_direction = left_picture_boat
fish_look_direction = left_picture_fish if fish.x_pos <= SIZE[0] // 2 else right_picture_fish

"""On screen shits :D"""
font = pygame.font.Font(None, 30)
try_count = 0
try_count_ = False
caught_fishes_count = 0
fps = int(1000 / pygame.time.Clock().tick(60))
# ------------------------
hitbox_fish = fish.hitbox

running = True
while running:
    pygame.time.Clock().tick(60)
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                hook.is_hook_moving = True

    seconds = pygame.time.get_ticks() // 1000  # NOQA
    if pygame.key.get_pressed()[pygame.K_a] and not hook.is_hook_moving:
        boat.move_left(seconds)
        fisherman_line.rotate_fisherman_left(boat)
        boat_look_direction = left_picture_boat
    elif pygame.key.get_pressed()[pygame.K_d] and not hook.is_hook_moving:
        boat.move_right(seconds, SIZE[0])
        fisherman_line.rotate_fisherman_right(boat)
        boat_look_direction = right_picture_boat

    if fish_look_direction == left_picture_fish:  # NOQA
        fish.swim_left(seconds)
        if fish.check_left_wall():
            fish_look_direction = right_picture_fish
    elif fish_look_direction == right_picture_fish:
        fish.swim_right(seconds)
        screen_width = SIZE[0]
        if fish.check_right_wall(screen_width):
            fish_look_direction = left_picture_fish

    line = pygame.Rect((fisherman_line.tip_of_the_rod, boat.y + 17, 1, fisherman_line.advance_line))
    fish_rect = pygame.Rect((fish.x_pos, fish.y_pos, 0, 0))
    hook_rect = pygame.Rect((fisherman_line.tip_of_the_rod, hook.y_pos, 0, 0))

    collide = fish_rect.colliderect(hook_rect)
    if collide:
        print("COLLISION")

    # print(hook_rect.x, hook_rect.y)
    # print(fish_rect.x, fish_rect.y)
    # print()

    if not hook.is_hook_moving:  # NOQA
        pygame.draw.rect(screen, (255, 0, 0), line)
    else:
        if not hook.bottom_reached:
            hook.drop_hook()
            if hook.bottom_reached:
                try_count += 1
        elif hook.bottom_reached:
            hook.get_hook_back(fisherman_line)
        pygame.draw.line(screen, (255, 0, 0), (fisherman_line.tip_of_the_rod, boat.y + 17),
                         (fisherman_line.tip_of_the_rod, hook.y_pos))

    screen.blit(boat_look_direction, (boat.x, boat.y))
    screen.blit(fish_look_direction, (fish.x_pos, fish.y_pos))
    """
    fisherman_line.tip_of_the_rod - 10 === hook knot position
    
    hook.y_pos if hook.is_hook_moving else fisherman_line.advance_line + 62
    hook.y_pos is the dynamic value
    boat.y + 160 is the value from the dynamically generated float boating
    """
    screen.blit(hook.picture, (fisherman_line.tip_of_the_rod - 10,
                               hook.y_pos if hook.is_hook_moving else boat.y + 160))

    text_fps = font.render(str(f"fps: {fps}"), True, (255, 0, 0))
    screen.blit(text_fps, (10, 10))
    text_try = font.render(str(f"try: {try_count}"), True, (255, 0, 0))
    screen.blit(text_try, (100, 10))
    caught_fishes = font.render(str(f"caught fishes: {caught_fishes_count}"), True, (255, 0, 0))
    screen.blit(caught_fishes, (175, 10))

    pygame.draw.rect(screen, (0, 0, 0), fish.hitbox, 2)
    # screen.blit(f, (fish.x_pos, fish.y_pos))

    pygame.display.flip()

data = ""
json_data = read_json()
json_data.update(data)
