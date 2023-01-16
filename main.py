import random
import pygame
from boat import Boat
from fish import Fish
from fishing_line import FishLine
from hook import Hook
from info_json import *


def random_fish_spawn():
    x = random.randrange(100, 1400)
    y = random.randrange(400, 800)
    return x, y


json_data = read_json()
SIZE = (1600, 900)
pygame.init()
screen = pygame.display.set_mode(SIZE)

background = pygame.image.load("images/background.png")
boat = Boat()

x_spawn, y_spawn = random_fish_spawn()
fish = Fish(x_spawn, y_spawn)
fish2 = Fish(200, 122)
fisherman_line = FishLine(boat)
hook = Hook(boat)

left_picture_boat, right_picture_boat = boat.load_boat()
left_picture_fish, right_picture_fish = fish.load_pictures()

boat_look_direction = left_picture_boat
fish_look_direction = left_picture_fish if fish.x_pos <= SIZE[0] // 2 else right_picture_fish

"""On screen shits"""
font = pygame.font.Font(None, 30)
caught_fishes_count = 0
fps = int(1000 / pygame.time.Clock().tick(60))
# ------------------------
fish_hitbox = pygame.Rect((fish.x_pos, fish.y_pos, 0, 0))  # NOQA
hook_hitbox = pygame.Rect((fisherman_line.tip_of_the_rod, hook.y_pos, 0, 0))  # NOQA
# caught_fish ---------------
caught_fish = pygame.image.load("images/fish_1_left.png")
caught_fish = pygame.transform.scale(caught_fish, (120, 80))
caught_fish = pygame.transform.rotate(caught_fish, -90)
# ----------------------------
running = True
is_fish_caught = False
while running:
    pygame.time.Clock().tick(60)

    screen.blit(background, (0, 0))
    text_fps = font.render(str(f"fps: {fps}"), True, (255, 0, 0))
    screen.blit(text_fps, (10, 10))
    caught_fishes = font.render(str(f"caught fishes: {boat.caught_fishes}"), True, (255, 0, 0))
    screen.blit(caught_fishes, (100, 10))
    info_record = font.render(str(f"previous record: {json_data['best_result']}"), True, (255, 0, 0))
    screen.blit(info_record, (280, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                hook.is_hook_moving = True

    if pygame.key.get_pressed()[pygame.K_a] and not hook.is_hook_moving:  # NOQA
        boat.move_left()
        fisherman_line.rotate_fisherman_left(boat)
        boat_look_direction = left_picture_boat
    elif pygame.key.get_pressed()[pygame.K_d] and not hook.is_hook_moving:
        boat.move_right(SIZE[0])
        fisherman_line.rotate_fisherman_right(boat)
        boat_look_direction = right_picture_boat

    seconds = pygame.time.get_ticks() // 1000  # NOQA

    transparent_surface = pygame.Surface((1600, 900))
    fish_hitbox_draw = pygame.draw.rect(transparent_surface, (0, 0, 0), (fish.x_pos, fish.y_pos + 27, 120, 40), 1)
    hook_hitbox.x, hook_hitbox.y = fisherman_line.tip_of_the_rod - 10, hook.y_pos
    hook_hitbox_draw = pygame.draw.rect(transparent_surface, (0, 0, 0), (hook_hitbox.x, hook_hitbox.y, 17, 33), 1)

    if fish_hitbox_draw.colliderect(hook_hitbox_draw):
        is_fish_caught = True
        fish_image = None
        fish_hitbox_draw = 0
        screen.blit(caught_fish, (hook_hitbox.x - 23, hook_hitbox.y + 20))
    if not is_fish_caught:
        if fish_look_direction == left_picture_fish:
            fish.swim_left(seconds, fish_hitbox)
            if fish.check_left_wall():
                fish_look_direction = right_picture_fish
        elif fish_look_direction == right_picture_fish:
            fish.swim_right(seconds, fish_hitbox)
            screen_width = SIZE[0]
            if fish.check_right_wall(screen_width):
                fish_look_direction = left_picture_fish
        line = pygame.Rect((fisherman_line.tip_of_the_rod, boat.y + 17, 1, fisherman_line.advance_line))
        if not hook.is_hook_moving:
            pygame.draw.rect(screen, (255, 0, 0), line)
        else:
            if not hook.bottom_reached:
                hook.drop_hook()
            elif hook.bottom_reached:
                hook.get_hook_back(fisherman_line)

            pygame.draw.line(screen, (255, 0, 0), (fisherman_line.tip_of_the_rod, boat.y + 17),
                             (fisherman_line.tip_of_the_rod, hook.y_pos))

        fish_image = screen.blit(fish_look_direction, (fish.x_pos, fish.y_pos))

    pygame.draw.line(screen, (255, 0, 0), (fisherman_line.tip_of_the_rod, boat.y + 17),
                     (fisherman_line.tip_of_the_rod, hook.y_pos))
    if is_fish_caught:
        screen.blit(caught_fish, (hook_hitbox.x - 23, hook_hitbox.y + 20))
        hook.caught_fish(fisherman_line)
        if hook.is_caught:
            fish.increase_speed_fish_after_caught()
            boat.caught_fish()
            is_fish_caught = False
            hook.fix_bug_fishing_every_second_time()
            x_spawn, y_spawn = random_fish_spawn()
            fish.x_pos, fish.y_pos = x_spawn, y_spawn

    screen.blit(boat_look_direction, (boat.x, boat.y))
    """
    fisherman_line.tip_of_the_rod - 10 === hook knot position
    hook.y_pos if hook.is_hook_moving else fisherman_line.advance_line + 62
    hook.y_pos is the dynamic value
    boat.y + 160 is the value from the dynamically generated float boating
    """
    screen.blit(hook.picture, (fisherman_line.tip_of_the_rod - 10,
                               hook.y_pos if hook.is_hook_moving else boat.y + 160))

    pygame.display.flip()

save_on_close(json_data, boat.caught_fishes)
