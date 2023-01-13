import pygame


class FishLine:
    __DROP_SPEED = 3
    __GET_BACK_SPEED = 6

    def __init__(self, start_point=(700, 100), end_point=(700, 200)):
        self.start_point = start_point
        self.end_point = end_point
        self.picture = pygame.image.load("images/hook.png")
        self.picture = pygame.transform.scale(self.picture, (15, 30))



