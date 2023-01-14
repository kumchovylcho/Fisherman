import pygame
from boat import Boat
from fish import Fish
from fishing_line import FishLine
from hook import Hook

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

running = True
while running:
    pygame.time.Clock().tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                hook.is_hook_moving = True

    seconds = pygame.time.get_ticks() // 1000
    if pygame.key.get_pressed()[pygame.K_a] and not hook.is_hook_moving:
        boat.move_left(seconds)
        fisherman_line.rotate_fisherman_left(boat)
        boat_look_direction = left_picture_boat
    elif pygame.key.get_pressed()[pygame.K_d] and not hook.is_hook_moving:
        boat.move_right(seconds, SIZE[0])
        fisherman_line.rotate_fisherman_right(boat)
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

    fish_rect = pygame.Rect((fish.x_pos, fish.y_pos, 0, 0))
    hook_rect = pygame.Rect((boat.x, boat.y, 0, 0))
    line = pygame.Rect((fisherman_line.tip_of_the_rod, boat.y + 17, 3, fisherman_line.advance_line))

    screen.blit(background, (0, 0))
    if not hook.is_hook_moving:
        pygame.draw.rect(screen, (255, 0, 0), line)
    else:
        if not hook.bottom_reached:
            hook.drop_hook()
        elif hook.bottom_reached:
            hook.get_hook_back(fisherman_line)
        pygame.draw.line(screen, (255, 0, 0), (fisherman_line.tip_of_the_rod, boat.y + 17),
                         (fisherman_line.tip_of_the_rod, hook.y_pos), 3)

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

    pygame.display.flip()
