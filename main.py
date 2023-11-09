import random
import pygame
from boat import Boat
from fish import Fish
from fishing_line import FishLine
from hook import Hook
from info_json import *
from utils import LEVELS, get_and_rotate_caught_fish, level_up

def random_fish_spawn():
    x = random.randrange(100, 1400)
    y = random.randrange(400, 800)
    return x, y


json_data = read_json()
SIZE = (1600, 900)
pygame.mixer.pre_init(44100, 16, 2, 4096)

pygame.init()
screen = pygame.display.set_mode(SIZE)

background = pygame.image.load("images/background.png")
background = pygame.transform.scale(background,(10000,900))

# Play Background Music
pygame.mixer.music.load('music/Background2.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Action Sound_SFX
caught_fish_sfx = pygame.mixer.Sound('music/sounds/caught_fish.mp3')
drop_hook_sfx = pygame.mixer.Sound('music/sounds/drop_hook2.mp3')

boat = Boat()

x_spawn, y_spawn = random_fish_spawn()
# fish = Fish(x_spawn, y_spawn, 0,)
fisherman_line = FishLine(boat)
hook = Hook(boat)

left_picture_boat, right_picture_boat = boat.load_boat()
boat_look_direction = left_picture_boat

def load_fish(level):
    f_width, f_height = LEVELS[level][2]
    fish = Fish(x_spawn, y_spawn, level, f_width, f_height)
    left_picture_fish, right_picture_fish = fish.load_pictures(level)
    fish_look_direction = left_picture_fish if fish.x_pos <= SIZE[0] // 2 else right_picture_fish

    return left_picture_fish, right_picture_fish, fish_look_direction, fish


left_picture_fish, right_picture_fish, fish_look_direction, fish = load_fish(0)

"""On screen shits"""
font = pygame.font.Font(None, 30)
caught_fishes_count = 0
fps = int(1000 / pygame.time.Clock().tick(60))
# ------------------------
fish_hitbox = pygame.Rect((fish.x_pos, fish.y_pos, 0, 0))  # NOQA
hook_hitbox = pygame.Rect((fisherman_line.tip_of_the_rod, hook.y_pos, 0, 0))  # NOQA


running = True
is_fish_caught = False
while running:
    pygame.time.Clock().tick(60)
    curr_level, leveled_up = level_up(boat.LEVEL, boat.caught_fishes)
    boat.LEVEL = curr_level

    if leveled_up:
        leveled_up = False
        left_picture_fish, right_picture_fish, fish_look_direction, fish = load_fish(curr_level)

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
                drop_hook_sfx.play()

    if (pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[
        pygame.K_LEFT]) and not hook.is_hook_moving:  # NOQA
        boat.move_left()
        fisherman_line.rotate_fisherman_left(boat)
        boat_look_direction = left_picture_boat

    elif (pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]) and not hook.is_hook_moving:
        boat.move_right(SIZE[0])
        fisherman_line.rotate_fisherman_right(boat)
        boat_look_direction = right_picture_boat

    seconds = pygame.time.get_ticks() // 1000  # NOQA

    transparent_surface = pygame.Surface((1600, 900))
    fish_hitbox_draw = pygame.draw.rect(transparent_surface, (0, 0, 0), (fish.x_pos, fish.y_pos + 27, 120, 40), 1)
    hook_hitbox.x, hook_hitbox.y = fisherman_line.tip_of_the_rod - 10, hook.y_pos
    hook_hitbox_draw = pygame.draw.rect(transparent_surface, (0, 0, 0), (hook_hitbox.x, hook_hitbox.y, 17, 33), 1)

    if fish_hitbox_draw.colliderect(hook_hitbox_draw):
        caught_fish_sfx.play()
        drop_hook_sfx.stop()
        is_fish_caught = True
        fish_image = None
        fish_hitbox_draw = 0
        caught_fish = get_and_rotate_caught_fish(curr_level, fish)
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
        caught_fish = get_and_rotate_caught_fish(curr_level, fish)
        screen.blit(caught_fish, (hook_hitbox.x - 23, hook_hitbox.y))
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
