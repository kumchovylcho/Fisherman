import pygame


class Boat:
    __MOVE_SPEED = 3
    # __MOVE_HORIZONTAL_DUE_WAVES = 0.18
    __BOAT_WIDTH = 250
    __BOAT_HEIGHT = 130

    def __init__(self, x=700, y=50):
        self.x = x
        self.y = y

    @staticmethod
    def load_boat():
        boat_left = pygame.image.load("images/boat_left.png")
        boat_left = pygame.transform.scale(boat_left, (Boat.__BOAT_WIDTH, Boat.__BOAT_HEIGHT))
        boat_right = pygame.image.load("images/boat_right.png")
        boat_right = pygame.transform.scale(boat_right, (Boat.__BOAT_WIDTH, Boat.__BOAT_HEIGHT))
        return boat_left, boat_right

    def move_left(self):
        if self.x > 0:
            self.x -= Boat.__MOVE_SPEED
            # if second_passed % 2 == 0:
            #     self.y -= Boat.__MOVE_HORIZONTAL_DUE_WAVES
            # else:
            #     self.y += Boat.__MOVE_HORIZONTAL_DUE_WAVES

    def move_right(self, screen_width: int):
        if self.x < screen_width - Boat.__BOAT_WIDTH:
            self.x += Boat.__MOVE_SPEED
            # if second_passed % 2 == 0:
            #     self.y -= Boat.__MOVE_HORIZONTAL_DUE_WAVES
            # else:
            #     self.y += Boat.__MOVE_HORIZONTAL_DUE_WAVES
