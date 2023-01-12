import pygame
from boat import Boat

SIZE = (1600, 900)
pygame.init()
screen = pygame.display.set_mode(SIZE)

background = pygame.image.load("images/background.png")

boat = Boat()
left_picture_boat, right_picture_boat = boat.load_boat()

running = True
look = left_picture_boat
while running:
    pygame.time.Clock().tick(60)
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.key.get_pressed()[pygame.K_a]:
        boat.move_left()
        look = left_picture_boat
    elif pygame.key.get_pressed()[pygame.K_d]:
        boat.move_right()
        look = right_picture_boat

    screen.blit(look, (boat.x, boat.y))
    pygame.display.update()
