import pygame

# List every nested list INDEX represent Level(1, 2, 3). Tuple represents experience (0exp, 100epx) => LevelUp => When surpassed)
# The string value is the name of image that has to be used.


MAX_LEVEL = 4
LEVELS = [
    [(0, 2), "fish", (120, 80)],
    [(3, 5), 'cyan', (180, 80)],
    [(6, 8), 'guard', (180, 100)],
    [(9, 11), 'boss', (180, 100)],
]


def flip_image(surface):
    flipped_surface = pygame.transform.flip(surface, True, False)
    return flipped_surface


def get_and_rotate_caught_fish(curr_level, fish):
    image = LEVELS[curr_level][1]
    caught_fish = pygame.image.load(f"images/Fish_types/{image}.png")
    caught_fish = pygame.transform.scale(caught_fish, (fish.fish_width, fish.fish_height))
    caught_fish = pygame.transform.rotate(caught_fish, 90)
    return caught_fish


def level_up(curr_level, caught_fishes):
    leveled_up = False
    max_exp_per_level = LEVELS[curr_level][0][1]
    if caught_fishes > max_exp_per_level:
        curr_level += 1
        leveled_up = True

    curr_level = min(curr_level, MAX_LEVEL)

    return curr_level, leveled_up



